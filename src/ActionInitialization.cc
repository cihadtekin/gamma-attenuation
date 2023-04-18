#include "ActionInitialization.hh"
#include "PrimaryGeneratorAction.hh"
#include "RunAction.hh"
#include "EventAction.hh"
#include "SteppingAction.hh"

namespace GammaAttenuation
{

ActionInitialization::ActionInitialization()
{}

ActionInitialization::~ActionInitialization()
{}

void ActionInitialization::BuildForMaster() const
{
  RunAction* runAction = new RunAction;
  SetUserAction(runAction);
}

void ActionInitialization::Build() const
{
  PrimaryGeneratorAction* generatorAction = new PrimaryGeneratorAction;
  RunAction* runAction = new RunAction;
  EventAction* eventAction = new EventAction(runAction);
  SteppingAction* steppingAction = new SteppingAction(eventAction);

  steppingAction->SetParticleGun(generatorAction->GetParticleGun());

  SetUserAction(generatorAction);
  SetUserAction(runAction);
  SetUserAction(eventAction);
  SetUserAction(steppingAction);
}

}
