#include "SteppingAction.hh"
#include "EventAction.hh"
#include "DetectorConstruction.hh"

#include "G4Step.hh"
#include "G4Event.hh"
#include "G4RunManager.hh"
#include "G4LogicalVolume.hh"

namespace GammaAttenuation
{

SteppingAction::SteppingAction(EventAction* eventAction)
: fEventAction(eventAction)
{}

SteppingAction::~SteppingAction()
{}

void SteppingAction::UserSteppingAction(const G4Step* step)
{
  const G4Track* track = step->GetTrack();

  const G4String modelName = track->GetCreatorModelName();
  const G4int modelId = track->GetCreatorModelID();
  const G4int modelIndex = track->GetCreatorModelIndex();

  const G4DynamicParticle* particle = track->GetDynamicParticle();
  // particle->DumpInfo();

  const G4ParticleDefinition* particleDef = track->GetParticleDefinition();
  const G4String particleName = particleDef->GetParticleName();

  G4cout
    << "STEP: "
    << particleName
    << G4endl;





  if (!fScoringVolume) {
    const DetectorConstruction* detConstruction
      = static_cast<const DetectorConstruction*>
        (G4RunManager::GetRunManager()->GetUserDetectorConstruction());
    fScoringVolume = detConstruction->GetScoringVolume();
  }

  // get volume of the current step
  G4LogicalVolume* volume
    = step->GetPreStepPoint()->GetTouchableHandle()
      ->GetVolume()->GetLogicalVolume();

  // check if we are in scoring volume
  if (volume != fScoringVolume) return;

  // collect energy deposited in this step
  G4double edepStep = step->GetTotalEnergyDeposit();
  fEventAction->AddEdep(edepStep);
}

}
