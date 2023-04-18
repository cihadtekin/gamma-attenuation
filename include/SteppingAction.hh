#ifndef GammaAttenuationSteppingAction_h
#define GammaAttenuationSteppingAction_h 1

#include "G4UserSteppingAction.hh"
#include "globals.hh"

class G4LogicalVolume;
class G4VPhysicalVolume;
class G4Box;
class G4ParticleGun;

namespace GammaAttenuation
{

class EventAction;

class SteppingAction : public G4UserSteppingAction
{
  public:
    SteppingAction(EventAction* eventAction);
    ~SteppingAction() override;

    // method from the base class
    void UserSteppingAction(const G4Step*) override;
    void SetParticleGun(const G4ParticleGun* particleGun) { fParticleGun = particleGun; }

  private:
    EventAction* fEventAction = nullptr;
    G4VPhysicalVolume* fAbsorberPhysical = nullptr;
    G4Box* fAbsorberSolid = nullptr;
    const G4ParticleGun* fParticleGun = nullptr; // pointer a to G4 gun class
};

}

#endif
