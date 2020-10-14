class TypeOfStatus:
    new = 'New'
    in_progress = 'InProgress'
    closed = 'Closed'
    cancelled = 'Cancelled'
    CHOICES = (
        (new, new),
        (in_progress, 'In Progress'),
        (cancelled, cancelled),
        (closed, closed),
    )
