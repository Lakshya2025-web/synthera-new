from ninja import NinjaAPI
from .auth import CustomAuth
api = NinjaAPI()

@api.get("/protected-check", auth=CustomAuth())
def protected_check(request):
    return {"message" : "protection check"}
