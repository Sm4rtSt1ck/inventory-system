from django.views.generic import TemplateView


class LoginView(TemplateView):
    template_name = 'frontend/login.html'


class EquipmentListView(TemplateView):
    template_name = 'frontend/equipment.html'


class EquipmentDetailView(TemplateView):
    template_name = 'frontend/equipment_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['equipment_id'] = self.kwargs['pk']
        return ctx


class AssignmentsView(TemplateView):
    template_name = 'frontend/assignments.html'


class LaboratoriesView(TemplateView):
    template_name = 'frontend/laboratories.html'


class PersonsView(TemplateView):
    template_name = 'frontend/persons.html'
