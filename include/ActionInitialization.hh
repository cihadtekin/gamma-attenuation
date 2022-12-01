#ifndef GammaAttenuationActionInitialization_h
#define GammaAttenuationActionInitialization_h 1

#include "G4VUserActionInitialization.hh"

/// Action initialization class.

namespace GammaAttenuation
{

class ActionInitialization : public G4VUserActionInitialization
{
  public:
    ActionInitialization();
    ~ActionInitialization() override;

    void BuildForMaster() const override;
    void Build() const override;
};

}

#endif
