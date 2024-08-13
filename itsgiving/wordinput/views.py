from django.shortcuts import render # Render a Django template (fill in {{}} gaps)
from django.http import JsonResponse # Return a JSON response to an HTTP request for AJAX (to be used in JavaScript engine of Browser)
from .forms import MainForm # Import the form class we definedfrom forms.py

from wordinput.ai_utils import get_closest_colleges_and_image_paths
from django.templatetags.static import static



def wordinput_view(request, university="cambridge"):
    if university not in ['oxford', 'cambridge']:
        university = 'cambridge'  # Default to Cambridge if an invalid university is provided

    # If the request is a POST request, then we want to process the form data
    # (Django expects usual HTML form submission to be a POST request)
    if request.method == 'POST':
        # Create our custom MainForm instance and populate it with data from the request
        form = MainForm(request.POST)

        # Check if the form is valid (i.e. if the input text is not empty, or any of our custom validation rules are not violated)
        if form.is_valid():
            # Django gives the cleaned_data attribute to the form object, which contains the validated input data (e.g. integers from strings, or our custom validation rules)
            search_input = form.cleaned_data['search_input']
            print(f"search_input: {search_input}")
            university = form.cleaned_data['university']
            print(f"university: {university}")
            undergrad_colleges_only = form.cleaned_data['undergrad_only']
            print(f"undergrad_colleges_only: {undergrad_colleges_only}")



            top_3_colleges_and_scores = get_closest_colleges_and_image_paths(search_input, university, undergrad_colleges_only)
            if top_3_colleges_and_scores is None:
                return JsonResponse({})
            else:
                college_1, college_image_path_1, college_score_1, college_2, college_image_path_2, college_score_2, college_3, college_image_path_3, college_score_3 = top_3_colleges_and_scores
        

            # XMLHttpRequest suggets that the request is an AJAX request (i.e. the form was submitted using JavaScript)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # Return a JSON response with the image path to the AJAX request (to be used in the JavaScript engine of the Browser)
                return JsonResponse({'college_1': college_1, 
                                     'college_image_path_1': static(college_image_path_1), 
                                     'college_score_1': college_score_1,
                                     'college_2': college_2, 
                                     'college_image_path_2': static(college_image_path_2), 
                                     'college_score_2': college_score_2,
                                     'college_3': college_3, 
                                     'college_image_path_3': static(college_image_path_3),
                                     'college_score_3': college_score_3})

        else:
            # If the form is not valid, return a JSON response no image path (so image is removed from the page)
            return JsonResponse({})
            
    else:
        # If the request is not a POST request, create a new form instance (i.e. the user has not submitted the form yet)
        form = MainForm()
        print("Passing University: ", university) # TODO remove
        return render(request, 'wordinput/wordinput_form.html', {'form': form, 'university': university})
