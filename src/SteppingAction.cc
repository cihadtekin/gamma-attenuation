#include "SteppingAction.hh"
#include "EventAction.hh"
#include "DetectorConstruction.hh"

#include "G4Step.hh"
#include "G4Event.hh"
#include "G4Box.hh"
#include "G4RunManager.hh"
#include "G4LogicalVolume.hh"
#include "G4ParticleGun.hh"

namespace GammaAttenuation
{

void logEvent(const G4Step * step) {
  const G4Track* track = step->GetTrack();

  // physics process that created this model
  const G4String modelName = track->GetCreatorModelName();
  const G4int modelId = track->GetCreatorModelID();
  const G4int modelIndex = track->GetCreatorModelIndex();

  // kinetic energy of the track
  const G4double kineticEnergy = track->GetKineticEnergy();

  // momentum of the track
  const G4ThreeVector momentumDirection = track->GetMomentumDirection();
  const double Py = momentumDirection.getY();
  const double Pz = momentumDirection.getZ();
  const double Px = momentumDirection.getX();

  // position of the track
  const G4ThreeVector position = track->GetPosition();
  const double Rx = position.getX();
  const double Ry = position.getY();
  const double Rz = position.getZ();

  // particle
  const G4DynamicParticle* particle = track->GetDynamicParticle();
  const G4ParticleDefinition* particleDef = track->GetParticleDefinition();
  const G4String particleName = particleDef->GetParticleName();
  // particle->DumpInfo();

  G4cout
    << "RX: " << Rx << " "
    << "RY: " << Ry << " "
    << "RZ: " << Rz << " " 
    << "PX: " << Px << " "
    << "PY: " << Py << " "
    << "PZ: " << Pz << " " 
    << "energy: " << kineticEnergy << " "
    << "process: " << modelName << " "
    << particleName
    << G4endl;
}

SteppingAction::SteppingAction(EventAction* eventAction)
: fEventAction(eventAction)
{}

SteppingAction::~SteppingAction()
{}

void SteppingAction::UserSteppingAction(const G4Step* step)
{
  // logEvent(step);
  const G4Track* track = step->GetTrack();
  const G4ThreeVector position = track->GetPosition();
  const G4double kineticEnergy = track->GetKineticEnergy();
  const double Rz = position.getZ();
  
  if (!fAbsorberPhysical) {
    const DetectorConstruction* detConstruction
      = static_cast<const DetectorConstruction*>
        (G4RunManager::GetRunManager()->GetUserDetectorConstruction());
    fAbsorberPhysical = detConstruction->GetAbsorberPhysical();
    fAbsorberSolid = detConstruction->GetAbsorberSolid();
  }

  const G4double halfOfTheTickness = fAbsorberSolid->GetZHalfLength();
  const G4ThreeVector vec = fAbsorberPhysical->GetObjectTranslation();
  const G4double absorberPosition = vec.getZ() - halfOfTheTickness; 
  const G4ThreeVector momentumDirection = track->GetMomentumDirection();
  const double Pz = momentumDirection.getZ();
  const G4double detectorPosition = 150;// TODO: fetch it from the geometry
  const G4double originalKineticEnergy = fParticleGun->GetParticleEnergy();
  // const G4double originalKineticEnergy = .5;// TODO: fetch it from definitions

  if (Pz < 0 || kineticEnergy != originalKineticEnergy) {
    return;
  }

  if (Rz == absorberPosition) {
    fEventAction->IncreaseBeamCount();
  } else if (Rz == detectorPosition) {
    fEventAction->IncreaseHitCount();
  }
}


}
