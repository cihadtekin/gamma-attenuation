#ifndef GammaAttenuationDetectorConstruction_h
#define GammaAttenuationDetectorConstruction_h 1

#include "G4VUserDetectorConstruction.hh"
#include "globals.hh"

class G4VPhysicalVolume;
class G4LogicalVolume; 
class G4Box;

namespace GammaAttenuation
{
class DetectorMessenger;

class DetectorConstruction : public G4VUserDetectorConstruction
{
  public:
    DetectorConstruction();
    ~DetectorConstruction() override;

    G4VPhysicalVolume* Construct() override;

    G4Box* GetAbsorberSolid() const { return fAbsorberSolid; }
    G4VPhysicalVolume* GetAbsorberPhysical() const { return fAbsorberPhysical; }

    void SetAbsorberMaterial(G4String);
    G4String GetAbsorberMaterial() const { return fAbsorberMaterial; }

    void SetAbsorberTickness(G4double);
    G4double GetAbsorberTickness() const { return fAbsorberTickness; }

  private:
    DetectorMessenger* fDetectorMessenger;
    G4String fAbsorberMaterial;
    G4double fAbsorberTickness;
    G4LogicalVolume* fAbsorberLogical;
    G4Box* fAbsorberSolid;
    G4VPhysicalVolume* fAbsorberPhysical;
};

}

#endif
