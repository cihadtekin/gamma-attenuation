#include "DetectorMessenger.hh"

#include "DetectorConstruction.hh"
#include "G4UIdirectory.hh"
#include "G4UIcmdWithAString.hh"
#include "G4UIcmdWithADoubleAndUnit.hh"
namespace GammaAttenuation
{

DetectorMessenger::DetectorMessenger(DetectorConstruction* det)
 : G4UImessenger(),
   fDetector(det),
   fDirectory(0),
   fSetMaterialCmd(0),
   fSetTicknessCmd(0)
{ 
  fDirectory = new G4UIdirectory("/GammaAttenuation/");
  fDirectory->SetGuidance("UI commands");

  fSetMaterialCmd = new G4UIcmdWithAString("/GammaAttenuation/setMaterial", this);
  fSetMaterialCmd->SetGuidance("Set material of the Absorber.");
  fSetMaterialCmd->SetParameterName("choice", false);
  fSetMaterialCmd->AvailableForStates(G4State_Idle);

  fSetTicknessCmd = new G4UIcmdWithADoubleAndUnit("/GammaAttenuation/setTickness", this); 
  fSetTicknessCmd->SetGuidance("Set tickness of the Absorber.");
  fSetTicknessCmd->SetParameterName("tickness", false);
  fSetTicknessCmd->AvailableForStates(G4State_Idle);
  fSetTicknessCmd->SetUnitCategory("Length");
  fSetTicknessCmd->SetRange("tickness>0");
}

DetectorMessenger::~DetectorMessenger()
{
  delete fSetMaterialCmd;
  delete fSetTicknessCmd;
  delete fDirectory;  
}

void DetectorMessenger::SetNewValue(G4UIcommand* command, G4String newValue)
{ 
  if (command == fSetMaterialCmd) {
    fDetector->SetAbsorberMaterial(newValue);
  } else if (command == fSetTicknessCmd) {
    fDetector->SetAbsorberTickness(fSetTicknessCmd
      ->GetNewDoubleValue(newValue));
  }
}

G4String DetectorMessenger::GetCurrentValue(G4UIcommand * command)
{
  G4String ans;

  if (command == fSetMaterialCmd) {
    ans = fDetector->GetAbsorberMaterial(); 
  } else if (command == fSetTicknessCmd) { 
    ans = fDetector->GetAbsorberTickness(); 
  }

  return ans;
}

}
