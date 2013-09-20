import json
import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from apps.ewatch.models import Class
from apps.ewatch.models import UpdateCheckClass

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@login_required
def class_coverage(request):
	c = {}
	c['total_classes'] = Class.objects.all().count()
	c['classes_scraped'] = len(set(UpdateCheckClass.objects.
								 values_list('class_pk__enrollware_id', 
											 flat=True)))
	return HttpResponse(json.dumps(c), content_type="application/json")