from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.views import generic

from bbsittingsharing.helpers import notify
from bbsittingsharing.models import BBSitting, Booking
from bbsittingsharing.forms import BBSittingForm

class LoginRequiredMixin(object):
    """Ensures the user is logged in to access the view"""
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class SearchView(LoginRequiredMixin, generic.ListView):
    """Searches all baby sittings close to a date"""
    model = BBSitting
    template_name = "bbsittingsharing/bbsitting_search.html"
    def get_queryset(self, *args, **kwargs):
        """Returns all BBSittings in a +/- 3 days range"""
        date = datetime.strptime(self.kwargs['date'], "%Y%m%d")
        delta = timedelta(days=3)
        return BBSitting.objects.filter(date__range=[date-delta, date+delta])

class CreateView(LoginRequiredMixin, generic.CreateView):
    """BBSitting creation view, saving the author"""
    model = BBSitting
    form_class = BBSittingForm
    def form_valid(self, form):
        """If the form is valid, save the associated models"""
        form.instance.author = self.request.user
        return super(CreateView, self).form_valid(form)

class BookView(LoginRequiredMixin, generic.TemplateView):
    """Creates a booking for the bbsitting and the user"""
    template_name="bbsittingsharing/book_confirm.html"
    def get(self, request, pk):
        bbsitting = BBSitting.objects.get(pk=pk)
        booking = Booking.objects.create(bbsitting=bbsitting, parent=request.user)
        notify(booking, request.user, 'book_request')
        return super(BookView, self).get(request, recipient=bbsitting.author.get_full_name())

class ValidateView(LoginRequiredMixin, generic.TemplateView):
    """Validates the booking"""
    template_name="bbsittingsharing/book_validate.html"
    def get(self, request, pk, booking_pk):
        booking = Booking.objects.get(pk=booking_pk)
        #check the bbsitting id and author
        if booking.bbsitting.pk != pk or booking.bbsitting.author != request.user:
            raise Http404
        booking.validated = True
        booking.save()
        notify(booking, request.user, 'book_validated')
        return super(ValidateView, self).get(request, booking=booking)

class FriendsView(LoginRequiredMixin, generic.ListView):
    """Shows the list of referers, referees, and members of the same group"""
    template_name="bbsittingsharing/friends_list.html"
    context_object_name = 'friends'
    def get(self, request, *args, **kwargs):
        self.user = request.user
        self.queryset = request.user.friends.all()
        return super(FriendsView, self).get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super(FriendsView, self).get_context_data(**kwargs)
        context['neighbours'] = self.user.groups.first().user_set.all()
        return context