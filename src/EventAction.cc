#include "EventAction.hh"
#include "RunAction.hh"

#include "G4Event.hh"
#include "G4RunManager.hh"

namespace GammaAttenuation
{

EventAction::EventAction(RunAction* runAction)
: fRunAction(runAction)
{}

EventAction::~EventAction()
{}

void EventAction::BeginOfEventAction(const G4Event*)
{
  hitCount = 0;
  beamCount = 0;
}

void EventAction::EndOfEventAction(const G4Event*)
{
  // accumulate statistics in run action
  fRunAction->AddHitCount(hitCount);
  fRunAction->AddBeamCount(beamCount);
}

}
