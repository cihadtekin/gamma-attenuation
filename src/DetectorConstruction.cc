#include "DetectorConstruction.hh"

#include "G4RunManager.hh"
#include "G4NistManager.hh"
#include "G4Box.hh"
#include "G4Cons.hh"
#include "G4Orb.hh"
#include "G4Sphere.hh"
#include "G4Trd.hh"
#include "G4LogicalVolume.hh"
#include "G4PVPlacement.hh"
#include "G4SystemOfUnits.hh"

namespace GammaAttenuation
{

DetectorConstruction::DetectorConstruction()
{}

DetectorConstruction::~DetectorConstruction()
{}

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
  G4VPhysicalVolume* world_phys = new G4PVPlacement(
    0,                //no rotation
    G4ThreeVector(),  //at (0,0,0)
    world_logic,      //its logical volume
    "World",          //its name
    0,                //its mother  volume
    false,            //no boolean operation
    0,                //copy number
    checkOverlaps     //overlaps checking
  );

  // Matrial
  G4double material_thickness = 30*mm;
  G4ThreeVector material_position = G4ThreeVector(0, 0, world_sizeZ/2 - 5*cm);
  G4Material* material_mat = nist->FindOrBuildMaterial("G4_Al");
  G4Box* material_solid = new G4Box(
    "World",          //its name
    0.5*world_sizeXY, //size x
    0.5*world_sizeXY, //size y 
    0.5*material_thickness   //size z
  );
  G4LogicalVolume* material_logic = new G4LogicalVolume(
    material_solid,
    material_mat,
    "Material"
  );
  new G4PVPlacement(
    0,
    material_position,
    material_logic,
    "Material",
    world_logic,
    false,
    0,
    checkOverlaps
  );

  fScoringVolume = material_logic;

  return world_phys;
}

}
