from datetime import timedelta, tzinfo

class UTC(tzinfo):
    """UTC"""
    def utcoffset(self, dt):
        return timedelta(hours=0)

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return timedelta(hours=0)

class EST(tzinfo):
    """EST"""
    def utcoffset(self, dt):
        return timedelta(hours=-4)

    def tzname(self, dt):
        return "EST"

    def dst(self, dt):
        return timedelta(hours=0)

class PST(tzinfo):
    """PST"""
    def utcoffset(self, dt):
        return timedelta(hours=-7)

    def tzname(self, dt):
        return "PST"

    def dst(self, dt):
        return timedelta(hours=0)