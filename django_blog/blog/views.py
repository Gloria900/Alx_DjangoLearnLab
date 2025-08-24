from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse

from .models import Post, Comment
from .forms import RegisterForm, PostForm, CommentForm

from taggit.models import Tag

from django.db.models import Q

# Handles user registration
# - Displays a registration form (GET request)
# - Saves new user and logs them in automatically (POST request)

def register_view(request):
  if request.method == 'POST':
    form = RegisterForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)  # Log in user after registration
      return redirect('profile')
  else:
    form = RegisterForm()
  return render(request, 'registration/register.html', {'form': form})

@login_required

# Handles user profile view & update
# - Requires login to access (@login_required)
# - Allows updating email address
@login_required
def profile_view(request):
  if request.method == 'POST':
    request.user.email = request.POST.get('email')
    request.user.save()
  return render(request, 'registration/profile.html')

# LIST: Anyone can view all posts. Ordered newest first.
class ListView(ListView):
  model = Post
  template_name = "blog/post_list.html"        # templates/blog/post_list.html
  context_object_name = "posts"
  ordering = ["-published_date"]
  paginate_by = 10  # optional

# DETAIL: Anyone can view a single post.
class DetailView(DetailView):
  model = Post
  template_name = "blog/post_detail.html"      # templates/blog/post_detail.html
  context_object_name = "post"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['comments'] = self.object.comments.all().order_by('-created_at')
    context['form'] = CommentForm()
    return context

  def post(self, request, *args, **kwargs):
    self.object = self.get_object()
    form = CommentForm(request.POST)
    if form.is_valid():
      comment = form.save(commit=False)
      comment.post = self.object
      comment.author = request.user
      comment.save()
      return redirect('post-detail', pk=self.object.pk)
    return self.get(request, *args, **kwargs)
  

class PostByTagListView(ListView):
  model = Post
  template_name = 'blog/post_list_by_tag.html'
  context_object_name = 'posts'

  def get_queryset(self):
    tag_slug = self.kwargs.get('tag_slug')
    self.tag = None
    if tag_slug:
      try:
        self.tag = Tag.objects.get(slug=tag_slug)
        return Post.objects.filter(tags__in=[self.tag])
      except Tag.DoesNotExist:
        return Post.objects.none()
    return Post.objects.all()

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['tag'] = self.tag
    return context

# CREATE: Only authenticated users can create.
# - author is set to request.user in form_valid()
class CreateView(LoginRequiredMixin, CreateView):
  model = Post
  form_class = PostForm
  template_name = "blog/post_form.html"        # used for both create & update

  def form_valid(self, form):
    # Bind the logged-in user as the author (not exposed on the form)
    form.instance.author = self.request.user
    return super().form_valid(form)

# UPDATE: Only the author can edit.
class UpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = Post
  form_class = PostForm
  template_name = "blog/post_form.html"

  def test_func(self):
    # Author-only access
    post = self.get_object()
    return post.author == self.request.user

# DELETE: Only the author can delete. Redirect to list on success.
class DeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = Post
  template_name = "blog/post_confirm_delete.html"
  success_url = reverse_lazy("post-list")

  def test_func(self):
    post = self.get_object()
    return post.author == self.request.user


class CommentCreateView(CreateView):
  model = Comment
  form_class = CommentForm
  template_name = 'blog/add_comment.html'

  def form_valid(self, form):
    post_pk = self.kwargs.get('pk')
    post = get_object_or_404(Post, pk=post_pk)
    
    form.instance.author = self.request.user
    form.instance.post = post
    return super().form_valid(form)

  def get_success_url(self):
    return reverse_lazy('post_detail', kwargs={'pk': self.kwargs.get('pk')})

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    post_pk = self.kwargs.get('pk')
    context['post'] = get_object_or_404(Post, pk=post_pk)
    return context

@method_decorator(login_required, name='dispatch')
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  """Allow comment authors to edit their comments."""
  model = Comment
  form_class = CommentForm
  template_name = 'blog/edit_comment.html'

  def test_func(self):
    comment = self.get_object()
    return self.request.user == comment.author

  def get_success_url(self):
    return reverse('post_detail', kwargs={'pk': self.object.post.pk})

@method_decorator(login_required, name='dispatch')
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  """Allow comment authors to delete their comments."""
  model = Comment
  template_name = 'blog/delete_comment.html'

  def test_func(self):
    comment = self.get_object()
    return self.request.user == comment.author

  def get_success_url(self):
    return reverse('post_detail', kwargs={'pk': self.object.post.pk})

def search(request):
  query = request.GET.get('q')
  results = Post.objects.filter(
    Q(title__icontains=query) | Q(content__icontains=query) | Q(tags__name__icontains=query)
  ).distinct()
  return render(request, 'blog/search_results.html', {'results': results, 'query': query})

class TaggedPostListView(ListView):
  model = Post
  template_name = 'blog/tagged_posts.html'
  context_object_name = 'posts'

  def get_queryset(self):
    return Post.objects.filter(tags__name=self.kwargs['tag_name'])