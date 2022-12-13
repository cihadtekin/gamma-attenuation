#ifndef GammaAttenuationSteppingAction_h
#define GammaAttenuationSteppingAction_h 1

#include "G4UserSteppingAction.hh"
#include "globals.hh"

class G4LogicalVolume;
class G4VPhysicalVolume;
class G4Box;

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

  private:
    EventAction* fEventAction = nullptr;
    G4VPhysicalVolume* fAbsorberPhysical = nullptr;
    G4Box* fAbsorberSolid = nullptr;
};

}

#endif
