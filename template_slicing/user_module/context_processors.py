from sliced.models import Diseases


def add_variable_to_context(request):
    if "cart" in request.session:
        a = len((request.session['cart']))
    else:
        a = 0
    return {
         'diseaseData': Diseases.objects.all(),
         'cartTotal': a
     }
