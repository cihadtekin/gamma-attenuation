#ifndef GammaAttenuationDetectorMessenger_h
#define GammaAttenuationDetectorMessenger_h 1

#include "G4UImessenger.hh"
#include "globals.hh"

class G4UIdirectory;
class G4UIcmdWithAString;
class G4UIcmdWithADoubleAndUnit;

namespace GammaAttenuation
{

class DetectorConstruction;

class DetectorMessenger: public G4UImessenger
{
  public:
    DetectorMessenger(DetectorConstruction* );
    ~DetectorMessenger();

    void SetNewValue(G4UIcommand*, G4String);
    G4String GetCurrentValue(G4UIcommand * command);
    
  private:
    DetectorConstruction*      fDetector;

    G4UIdirectory*             fDirectory;
    G4UIcmdWithAString*        fSetMaterialCmd;
    G4UIcmdWithADoubleAndUnit* fSetTicknessCmd;
};

}

#endif

