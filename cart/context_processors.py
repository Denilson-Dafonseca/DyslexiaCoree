from .cart import Cart

# Create context 
def cart(request):
	# Return the default data 
	return {'cart': Cart(request)}