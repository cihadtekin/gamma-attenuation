#ifndef GammaAttenuationEventAction_h
#define GammaAttenuationEventAction_h 1

#include "G4UserEventAction.hh"
#include "globals.hh"

/// Event action class

namespace GammaAttenuation
{

class RunAction;

class EventAction : public G4UserEventAction
{
  public:
    EventAction(RunAction* runAction);
    ~EventAction() override;

    void BeginOfEventAction(const G4Event* event) override;
    void EndOfEventAction(const G4Event* event) override;

    void AddEdep(G4double edep) { fEdep += edep; }

  private:
    RunAction* fRunAction = nullptr;
    G4double   fEdep = 0.;
};

}

#endif

