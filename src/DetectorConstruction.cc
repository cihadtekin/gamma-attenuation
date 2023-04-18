#include "DetectorConstruction.hh"

#include "DetectorMessenger.hh"
#include "G4Material.hh"
#include "G4RunManager.hh"
#include "G4NistManager.hh"
#include "G4Box.hh"
#include "G4LogicalVolume.hh"
#include "G4PVPlacement.hh"
#include "G4SystemOfUnits.hh"

namespace GammaAttenuation
{

DetectorConstruction::DetectorConstruction()
: G4VUserDetectorConstruction(),
  fAbsorberMaterial("G4_Fe"),
  fAbsorberTickness(20 * mm),
  fDetectorMessenger(0),
  fAbsorberLogical(0),
  fAbsorberSolid(0),
  fAbsorberPhysical(0)
{
  fDetectorMessenger = new DetectorMessenger(this);
}

DetectorConstruction::~DetectorConstruction()
{
  delete fDetectorMessenger;
}

void DetectorConstruction::SetAbsorberMaterial(G4String materialChoice)
{
  G4NistManager* nist = G4NistManager::Instance();
  G4Material* absorberMaterialObject = nist->FindOrBuildMaterial(materialChoice);

  if (absorberMaterialObject)
  {
    fAbsorberMaterial = materialChoice;
    fAbsorberLogical->SetMaterial(absorberMaterialObject);
  }
  else
  { 
    G4cerr 
      << materialChoice << " is not defined. - Command is ignored." << G4endl; 
  }
}

void DetectorConstruction::SetAbsorberTickness(G4double tickness)
{
  if (tickness < 200 && tickness > 0) 
  {
    fAbsorberTickness = tickness;
    fAbsorberSolid->SetZHalfLength(tickness/2.);
    G4RunManager::GetRunManager()->GeometryHasBeenModified();
    // G4cout << "tickness set to " << tickness << G4endl;
  }
  else
  {
    G4cerr << "tickness needs to be in range of 0-50mm" << G4endl;
  }
}

G4VPhysicalVolume* DetectorConstruction::Construct()
{
  // Get nist material manager
  G4NistManager* nist = G4NistManager::Instance();

  // Option to switch on/off checking of volumes overlaps
  G4bool checkOverlaps = true;

  // World
  G4double world_sizeXY = 20*cm, world_sizeZ = 30*cm;
  G4Material* world_mat = nist->FindOrBuildMaterial("G4_AIR");
  G4Box* world_solid = new G4Box(
    "World",          //its name
    0.5*world_sizeXY, //size x
    0.5*world_sizeXY, //size y 
    0.5*world_sizeZ   //size z
  );
  G4LogicalVolume* world_logic = new G4LogicalVolume(
    world_solid,      //its solid
    world_mat,        //its material
    "World"           //its name
  );
  G4VPhysicalVolume* fWorldPhysical = new G4PVPlacement(
    0,                //no rotation
    G4ThreeVector(),  //at (0,0,0)
    world_logic,      //its logical volume
    "World",          //its name
    0,                //its mother  volume
    false,            //no boolean operation
    0,                //copy number
    checkOverlaps     //overlaps checking
  );

  // Absorber
  G4ThreeVector absorber_position = G4ThreeVector(0, 0, 0);
  G4Material* absorber_material = nist->FindOrBuildMaterial(fAbsorberMaterial);
  fAbsorberSolid = new G4Box(
    "World",          //its name
    0.5*world_sizeXY, //size x
    0.5*world_sizeXY, //size y 
    0.5*fAbsorberTickness   //size z
  );
  fAbsorberLogical = new G4LogicalVolume(
    fAbsorberSolid,
    absorber_material,
    "Absorber"
  );
  fAbsorberPhysical = new G4PVPlacement(
    0,
    absorber_position,
    fAbsorberLogical,
    "Absorber",
    world_logic,
    false,
    0,
    checkOverlaps
  );

  return fWorldPhysical;
}

}
