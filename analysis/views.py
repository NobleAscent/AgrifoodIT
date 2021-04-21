from django.http import JsonResponse

from analysis.rohit.pig_enhanced_FPmining import generate_dataset_fpmining


def pig_enhanced_FPmining(request):
    generate_dataset_fpmining(num_of_pressure_ranges=5, num_of_hum_ranges=5, num_of_temp_ranges=5, time_range=180,
                              support_threshold=0.1, conf_threshold=0.1, lift_threshold=0.1)
    return JsonResponse({'status': 'success'})