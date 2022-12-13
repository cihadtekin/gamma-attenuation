#ifndef GammaAttenuationEventAction_h
#define GammaAttenuationEventAction_h 1

#include "G4UserEventAction.hh"
#include "globals.hh"

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

    void IncreaseHitCount() {
      hitCount++;
    }

    void IncreaseBeamCount() {
      beamCount++;
    }

  private:
    RunAction* fRunAction = nullptr;
    G4int      hitCount = 0;
    G4int      beamCount = 0;
};

}

#endif

