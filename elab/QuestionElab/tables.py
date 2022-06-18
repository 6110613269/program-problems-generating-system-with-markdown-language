import django_tables2 as tables
from .models import Question
from django_tables2.utils import A

class MyColumn(tables.Column): 
    empty_values = list() 
    def render(self, value, record):
        return mark_safe('<button id="%s" class="btn btn-info">Submit</button>' % escape(record.id))

class QuestionTable(tables.Table):
    # idq = tables.Column(accessor='id')
    # T1     = "<a href='home/1' class='btn btn-primary text-xs' >update</a>"
    T1     = "<button type='button' class='btn js-update' update-link={{ record.get_absolute_url_update }}>update</button>"
    T2     = "<button type='button' class='btn js-delete' delete-link={{ record.get_absolute_url_delete }}>delete</button>"
    # name = = tables.LinkColumn('index', args=[A('id')], attrs={ 'a': {'class': 'btn'})}
    # delete = = tables.LinkColumn('main:delete_item', args=[A('pk')], attrs={ 'a': {'class': 'btn'} })
    
    


    # class PersonTable(tables.Table):name = tables.Column()
    # country = tables.RelatedLinkColumn()
    # continent = tables.RelatedLinkColumn(accessor="country.continent")
    
    edit   = tables.TemplateColumn(T1)
    delete = tables.TemplateColumn(T2)
    
    


    class Meta:
        model = Question
        template_name = "django_tables2/bootstrap4.html"
        fields = ("question_name", "question_language")
        
