from django.http import JsonResponse

from analysis.rohit.presence_FPmining import mergePresenceWithWeather, findPigEntryExit, total_count_of_occurrences


def pig_enhanced_FPmining(request):
    total_count_of_occurrences()
    return JsonResponse({'status': 'success'})