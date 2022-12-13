#ifndef GammaAttenuationRunAction_h
#define GammaAttenuationRunAction_h 1

#include "G4UserRunAction.hh"
#include "G4Accumulable.hh"
#include "globals.hh"

class G4Run;

namespace GammaAttenuation
{

class RunAction : public G4UserRunAction
{
  public:
    RunAction();
    ~RunAction() override;

    void BeginOfRunAction(const G4Run*) override;
    void   EndOfRunAction(const G4Run*) override;

    void AddHitCount(G4int _hitCount) {
      hitCount += _hitCount; 
    }
    void AddBeamCount(G4int _beamCount) {
      beamCount += _beamCount; 
    }

  private:
    G4Accumulable<G4int> hitCount = 0;
    G4Accumulable<G4int> beamCount = 0;
};

}

#endif

