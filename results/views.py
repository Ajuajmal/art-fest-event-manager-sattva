from django.shortcuts import render

from .models import EventsResult,BranchPoint

def point_lists(request):
        score = BranchPoint.objects.all()
        winners = EventsResult.objects.all()
        ce =0
        cse = 0
        ec = 0
        eee = 0
        it = 0
        me = 0
        me = 0
        mca = 0
        for x in score :
            if x.branch == 0:
                ce +=x.score
            if x.branch == 1:
                cse +=x.score
            if x.branch == 2:
                ec +=x.score
            if x.branch == 3:
                eee +=x.score
            if x.branch == 4:
                it +=x.score
            if x.branch == 5:
                me +=x.score
            if x.branch == 6:
                mca +=x.score

        return render(request, "home.html", {
                "ce": ce,
                "cse": cse,
                "ec": ec,
                "eee": eee,
                "it": it,
                "me": me,
                "mca": mca,
                "winners":winners
            })
