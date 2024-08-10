from django.shortcuts import render # Render a Django template (fill in {{}} gaps)
from django.http import JsonResponse # Return a JSON response to an HTTP request for AJAX (to be used in JavaScript engine of Browser)
from .forms import TextInputForm # Import the form class we definedfrom forms.py

# This function will select an image based on the input text 
def select_image(text):

    # TODO add ai stuff soon
    # college_name = "cambridge_jesus"
    number_from_text = int(text)
    

    image_path = f'wordinput/{college_name}.svg'
    return image_path


def wordinput_view(request):

    # If the request is a POST request, then we want to process the form data
    # (Django expects usual HTML form submission to be a POST request)
    if request.method == 'POST':
        # Create our custom TextInputForm instance and populate it with data from the request
        form = TextInputForm(request.POST)

        # Check if the form is valid (i.e. if the input text is not empty, or any of our custom validation rules are not violated)
        if form.is_valid():
            # Django gives the cleaned_data attribute to the form object, which contains the validated input data (e.g. integers from strings, or our custom validation rules)
            text = form.cleaned_data['text']
            image_path = select_image(text)
            
            # XMLHttpRequest suggets that the request is an AJAX request (i.e. the form was submitted using JavaScript)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # Return a JSON response with the image path to the AJAX request (to be used in the JavaScript engine of the Browser)
                return JsonResponse({'image_path': f'static/{image_path}'})
            else:
                # If the request was not an AJAX request, render the template with the form and the image path
                # (For backup if JavaScript is disabled in the Browser)
                return render(request, 'wordinput/wordinput_form.html', {'form': form, 'image_path': image_path})
        else:
            # If the form is not valid, return a JSON response no image path (so image is removed from the page)
            return JsonResponse({})
            
    else:
        # If the request is not a POST request, create a new form instance (i.e. the user has not submitted the form yet)
        form = TextInputForm()
        return render(request, 'wordinput/wordinput_form.html', {'form': form})
