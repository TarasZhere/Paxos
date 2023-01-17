class Promise:
    def __init__(self, id, latestProposal=None, latestValue=None) -> None:
        self.id = id
        self.promise = False
        self.latestProposal = latestProposal
        self.latestValue = latestValue
        pass

    def get(self):
        return self.promise, self.latestProposal, self.latestValue