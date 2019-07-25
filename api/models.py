from django.db import models

# Create your models here.
class Project(models.Model):
    id = models.CharField(max_length=8,primary_key=True,unique=True,verbose_name='项目编号')
    name = models.CharField(max_length=20,verbose_name='项目名称')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    class Meta:
        db_table = 'project'
        verbose_name = '项目'
        verbose_name_plural = '项目'
    def __str__(self):
        return self.name


class RuleInfo(models.Model):
    uid = models.CharField(max_length=8,primary_key=True,unique=True,verbose_name='UID')
    name = models.CharField(max_length=50,verbose_name='名称')
    desc = models.CharField(max_length=200,verbose_name='描述',null=True,blank=True)
    request_body = models.TextField(verbose_name='请求',null=True,blank=True)
    response_body = models.TextField(verbose_name='响应')
    proxy = models.CharField(max_length=20,verbose_name='转发代理',null=True,blank=True)
    priority = models.IntegerField(verbose_name='优先级')
    project = models.ForeignKey(Project,models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    class Meta:
        db_table = 'rule'
        verbose_name = '规则'
        verbose_name_plural = '规则'
    def __str__(self):
        return self.name
class History(models.Model):
    id = models.CharField(max_length=20,primary_key=True, unique=True, verbose_name='编号')
    rule = models.TextField(verbose_name='规则')
    request_body = models.TextField(verbose_name='请求')
    response_body = models.TextField(verbose_name='响应')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    class Meta:
        db_table = 'history'
        verbose_name = '历史记录'
        verbose_name_plural = '历史记录'
    def __str__(self):
        return self.id