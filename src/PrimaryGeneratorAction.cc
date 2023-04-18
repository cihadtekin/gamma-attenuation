#include "PrimaryGeneratorAction.hh"

#include "G4LogicalVolumeStore.hh"
#include "G4LogicalVolume.hh"
#include "G4Box.hh"
#include "G4RunManager.hh"
#include "G4ParticleGun.hh"
#include "G4ParticleTable.hh"
#include "G4ParticleDefinition.hh"
#include "G4SystemOfUnits.hh"
#include "Randomize.hh"

namespace GammaAttenuation
{

PrimaryGeneratorAction::PrimaryGeneratorAction()
{
  G4int n_particle = 1;
  fParticleGun  = new G4ParticleGun(n_particle);

  // default particle kinematic
  G4ParticleTable* particleTable = G4ParticleTable::GetParticleTable();
  G4String particleName;
  G4ParticleDefinition* particle
    = particleTable->FindParticle(particleName="gamma");
  fParticleGun->SetParticleDefinition(particle);
  fParticleGun->SetParticleMomentumDirection(G4ThreeVector(0.,0.,1.));
  fParticleGun->SetParticleEnergy(662*keV);
}

PrimaryGeneratorAction::~PrimaryGeneratorAction()
{
  delete fParticleGun;
}

void PrimaryGeneratorAction::GeneratePrimaries(G4Event* anEvent)
{
  //this function is called at the begining of ecah event

  // In order to avoid dependence of PrimaryGeneratorAction
  // on DetectorConstruction class we get World volume
  // from G4LogicalVolumeStore.

  G4double worldSizeXY = 0;
  G4double worldSizeZ = 0;

  if (!fWorldBox)
  {
    G4LogicalVolume* worldLV
      = G4LogicalVolumeStore::GetInstance()->GetVolume("World");
    if ( worldLV ) fWorldBox = dynamic_cast<G4Box*>(worldLV->GetSolid());
  }

  if ( fWorldBox ) {
    worldSizeXY = fWorldBox->GetXHalfLength()*2.;
    worldSizeZ = fWorldBox->GetZHalfLength()*2.;
  }
  else  {
    G4ExceptionDescription msg;
    msg << "World volume of box shape not found.\n";
    msg << "Perhaps you have changed geometry.\n";
    msg << "The gun will be place at the center.";
    G4Exception("PrimaryGeneratorAction::GeneratePrimaries()",
     "MyCode0002",JustWarning,msg);
  }

  G4double size = 0.8;
  G4double x0 = size * worldSizeXY * (G4UniformRand()-0.5);
  G4double y0 = size * worldSizeXY * (G4UniformRand()-0.5);
  G4double z0 = -0.5 * worldSizeZ;

  fParticleGun->SetParticlePosition(G4ThreeVector(x0,y0,z0));

  fParticleGun->GeneratePrimaryVertex(anEvent);
}

}


