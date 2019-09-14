from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
# 如果修改此models.py文件，需要输入两条命令
# 1、python manage.py makemigrations blog 创建新的迁移。
# 2、python manage.py migrate 使数据库与模型保持同步。


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    # slug 这个字段其实就是用在文章的URL的。比如你现在一篇文章的标题是“i like django”,
    # 你可以把slug设置成"i-like-django",然后显示在浏览器的地址URL就是比如这样www.example.com/article/i-like-django/
    # 因为每个文章都是唯一的，这个slug也一定要唯一，所以你在里面设置的参数是unique=True。
    # 每篇文章的URL地址都是后面跟他的文章唯一id，你看你的这篇帖子的URL是http://www.fanhuaxiu.com/article/852/
    # 因为你这篇文章的ID是852
    # 这样我在处理文章的一些其他的操作就很简单，直接根据这个ID就能在数据库里面找到这个文章。
    # 反正slug就是这么个功能，对网站的SEO有好处吧。看你自己需求，要不要用，怎么用，看你了。
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    #  on_delete=models.CASCADE,----在创建多对一的关系的,需要在Foreign的第二参数中加入on_delete=models.CASCADE
    # 主外关系键中，级联删除，也就是当删除主表的数据时候从表中的数据也随着一起删除
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')

    class Meta:
        ordering = ('-publish',)

    # 打印一个实例化对象时，打印的其实是一个对象的地址。而通过__str__()函数就可以帮助我们打印对象中具体的属性值，
    # 或者你想得到的东西。
    # 因为在python中调用print()打印实例化对象时会调用__str__()，如果__str__()中有返回值，就会打印其中的返回值。
    def __str__(self):
        return self.title