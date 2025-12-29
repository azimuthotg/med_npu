from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import News, Category


class NewsListView(ListView):
    """รายการข่าวทั้งหมด"""
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = News.objects.filter(is_published=True)
        
        # Filter by category
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        return queryset.select_related('category')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        
        # Current category
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            context['current_category'] = get_object_or_404(Category, slug=category_slug)
        
        # Featured news
        context['featured_news'] = News.objects.filter(
            is_published=True, 
            is_featured=True
        )[:3]
        
        return context


class NewsDetailView(DetailView):
    """รายละเอียดข่าว"""
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Increment view count
        obj.increment_view()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Related news (same category)
        if self.object.category:
            context['related_news'] = News.objects.filter(
                is_published=True,
                category=self.object.category
            ).exclude(pk=self.object.pk)[:4]
        else:
            context['related_news'] = News.objects.filter(
                is_published=True
            ).exclude(pk=self.object.pk)[:4]
        
        return context
