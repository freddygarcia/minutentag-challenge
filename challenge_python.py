"""
Refactor the next function using yield to return the array of objects found by the
`s3.list_objects_v2` function that matches the given prefix.
"""
def get_s3_objects(bucket, prefix=''):
    s3 = boto3.client('s3')

    kwargs = {'Bucket': bucket}
    next_token = None
    if prefix:
        kwargs['Prefix'] = prefix
    while True:
        if next_token:
            kwargs['ContinuationToken'] = next_token
        resp = s3.list_objects_v2(**kwargs)
        contents = resp.get('Contents', [])
        for obj in contents:
            key = obj['Key']
            if key.startswith(prefix):
                yield obj
        next_token = resp.get('NextContinuationToken', None)

        if not next_token:
            break

"""
Please, full explain this function: document iterations, conditionals, and the
function as a whole
"""
def fn(main_plan, obj, extensions=[]):

    # From the extensions array, we are creating a dictionary with the price id as key and the quantity as value.
    # For each item in the cart, we want to check if the item price is in the main plan or in the extensions.
    # If the item does not exist in the main plan or in the extensions, the item is labeled as deleted.
    # If the item exists in the extensions, we check if the quantity is less than 1, if so, the item is labeled as deleted, otherwise
    # the item is labeled with the quantity.
    # When the item is in the main plan, we set the sp flag to True, so we know that the main plan is in the cart.
    # After we check the item, we remove the item from the extensions dictionary, so we know that the item was already checked.
    # Finally, if no main plan was found in the cart, we add the main plan to the cart with a quantity of 1. The purpose of this is to make sure that the main plan is always in the cart.
    # Then we proceed to add the rest of the items in the extensions dictionary to the cart with their respective quantities.

    items = []
    sp = False
    cd = False

    ext_p = {}

    for ext in extensions:
        ext_p[ext['price'].id] = ext['qty']

    for item in obj['items'].data:
        product = {
            'id': item.id
        }

        if item.price.id != main_plan.id and item.price.id not in ext_p:
            product['deleted'] = True
            cd = True
        elif item.price.id in ext_p:
            qty = ext_p[item.price.id]
            if qty < 1:
                product['deleted'] = True
            else:
                product['qty'] = qty
            del ext_p[item.price.id]
        elif item.price.id == main_plan.id:
            sp = True


        items.append(product)
    
    if not sp:
        items.append({
            'id': main_plan.id,
            'qty': 1
        })
    
    for price, qty in ext_p.items():
        if qty < 1:
            continue
        items.append({
            'id': price,
            'qty': qty
        })
    
    return items


"""
Having the class `Caller` and the function `fn`
Refactor the function `fn` to execute any method from `Caller` using the argument `fn_to_call`
reducing the `fn` function to only one line.
"""
class Caller:
    add = lambda a, b : a + b
    concat = lambda a, b : f'{a},{b}'
    divide = lambda a, b : a / b
    multiply = lambda a, b : a * b

def fn(fn_to_call, *args):
    return getattr(Caller, fn_to_call)(*args)


"""
A video transcoder was implemented with different presets to process different videos in the application. The videos should be
encoded with a given configuration done by this function. Can you explain what this function is detecting from the params
and returning based in its conditionals?
"""
def fn(config, w, h):
    """
    Based on the width and height, this function is calculating the aspect ration of the video (as).

    When the aspect ratio is less than 1, this means the video is in portrait orientation. For that
    reason makes sense to me that the preset choosen is 'p'.

    When the aspect ratio is bigger than than 1, but less than 4/3, this means the video is in widescreen format (e.g. HD (1280x720)).
    Makes sense that the preset choosen is 'l' (for large).

    Aspect ratios greater than 4/3 means the video is too wide, so we opted for a smaller preset 's'.

    Then the function returns the proper array of presets.

    """
    v = None
    ar = w / h

    if ar < 1:
        v = [r for r in config['p'] if r['width'] <= w]
    elif ar > 4 / 3:
        v = [r for r in config['l'] if r['width'] <= w]
    else:
        v = [r for r in config['s'] if r['width'] <= w]

    return v

"""
Having the next helper, please implement a refactor to perform the API call using one method instead of rewriting the code
in the other methods.
"""
import requests
class Helper:
    DOMAIN = 'http://example.com'
    SEARCH_IMAGES_ENDPOINT = 'search/images'
    GET_IMAGE_ENDPOINT = 'image'
    DOWNLOAD_IMAGE_ENDPOINT = 'downloads/images'

    AUTHORIZATION_TOKEN = {
        'access_token': None,
        'token_type': None,
        'expires_in': 0,
        'refresh_token': None
    }

    def _request(self, endpoint, method, **kwargs):
        token_type = self.AUTHORIZATION_TOKEN['token_type']
        access_token = self.AUTHORIZATION_TOKEN['access_token']

        headers = {
            'Authorization': f'{token_type} {access_token}',
        }

        URL = f'{self.DOMAIN}/{endpoint}'

        send = {
            'headers': headers,
            **kwargs
        }

        request_method = getattr(requests, method, None)

        if request_method:
            response = request_method(URL, **send)
        else:
            raise ValueError("Unsupported HTTP method")

        return response

    def search_images(self, **kwargs):
        return self._request(self.SEARCH_IMAGES_ENDPOINT, method='get', params=kwargs)

    def get_image(self, image_id, **kwargs):
        endpoint = f'{self.GET_IMAGE_ENDPOINT}/{image_id}'
        return self._request(endpoint, method='get', params=kwargs)

    def download_image(self, image_id, **kwargs):
        endpoint = f'{self.DOWNLOAD_IMAGE_ENDPOINT}/{image_id}'
        return self._request(endpoint, method='post', data=kwargs)

