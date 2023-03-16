from resources.auth import RegisterResource, LoginResource
from resources.complaint import ComplaintsResource, ComplaintApproveResources, ComplaintRejectResources

routes = (
    (RegisterResource, '/register'),
    (LoginResource, '/login'),
    (ComplaintsResource, '/complaints'),
    # TODO: new URL for single complaint
    (ComplaintApproveResources, '/complaints/<int:pk>/approve'),
    (ComplaintRejectResources, '/complaints/<int:pk>/reject')
)
