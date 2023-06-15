#include "DetectorConstruction.hh"
#include "ActionInitialization.hh"
#include "G4AccumulableManager.hh"

#include "G4RunManagerFactory.hh"
#include "G4SteppingVerbose.hh"
#include "G4UImanager.hh"
#include "QBBC.hh"

#include "G4VisExecutive.hh"
#include "G4UIExecutive.hh"

#include "Randomize.hh"
#include <fstream>
#include <cstdlib>

using namespace GammaAttenuation;

void calculateHVL(G4RunManager * runManager, G4UImanager * uiManager, int argc, char* argv[])
{
  G4AccumulableManager* accumulableManager = G4AccumulableManager::Instance();

  std::ofstream outfile("result.csv");

  G4String material = argv[1];
  G4String beamEnergyValue = argv[2];
  G4String beamEnergyUnit = argv[3];
  int initialBeamCount = atoi(argv[4]); // 10000
  int measurementCount = atoi(argv[5]); // 20
  double min = atof(argv[6]);
  double max = atof(argv[7]);
  double deltaT = (max - min) / measurementCount;

  outfile << "thickness (cm);count" << std::endl;

  for (size_t i = 1; i <= measurementCount; i++)
  {
    double thickness = min + i * deltaT;

    uiManager->ApplyCommand("/run/initialize");
    uiManager->ApplyCommand("/GammaAttenuation/setMaterial " + material);
    uiManager->ApplyCommand("/GammaAttenuation/setTickness " + std::to_string(thickness) + " cm");
    uiManager->ApplyCommand("/gun/particle gamma");
    uiManager->ApplyCommand("/gun/energy " + beamEnergyValue + " " + beamEnergyUnit);
    uiManager->ApplyCommand("/run/beamOn " + std::to_string(initialBeamCount));

    G4Accumulable<G4int>* hitCount = accumulableManager->GetAccumulable<G4int>("hitCount");
    G4cout << "thickness: " << std::to_string(thickness) + " cm, "
      << "count: " << hitCount->GetValue() << G4endl;
    outfile << thickness << ";" << hitCount->GetValue() << std::endl;
  }

  outfile.close();
}

int main(int argc, char* argv[])
{
  // Detect interactive mode (if no arguments) and define UI session
  G4UIExecutive* ui = nullptr;
  if (argc == 1) { ui = new G4UIExecutive(argc, argv); }

  // Optionally: choose a different Random engine...
  // G4Random::setTheEngine(new CLHEP::MTwistEngine);

  //use G4SteppingVerboseWithUnits
  G4int precision = 4;
  G4SteppingVerbose::UseBestUnit(precision);

  // Construct the default run manager
  auto* runManager = G4RunManagerFactory::CreateRunManager(G4RunManagerType::Default);

  // Set mandatory initialization classes
  // Detector construction
  runManager->SetUserInitialization(new DetectorConstruction());
  G4VModularPhysicsList* physicsList = new QBBC;
  runManager->SetUserInitialization(physicsList);
  runManager->SetUserInitialization(new ActionInitialization());

  // Initialize visualization
  G4VisManager* visManager = new G4VisExecutive();
  visManager->Initialize();

  // Get the pointer to the User Interface manager
  G4UImanager* uiManager = G4UImanager::GetUIpointer();

  runManager->Initialize();

  // Process macro 
  if (!ui) {
    G4String arg1 = argv[1];

    if (argc == 2) {
      uiManager->ApplyCommand("/control/execute " + arg1);
    } else {
      calculateHVL(runManager, uiManager, argc, argv);
    }
    // if (arg == "hvl") {
    //   calculateHVL(runManager, uiManager);
    // } else {
    //   uiManager->ApplyCommand("/control/execute " + arg);
    // }
  } else { // interactive mode
    uiManager->ApplyCommand("/control/execute vis.mac");
    ui->SessionStart();
    delete ui;
  }

  // Job termination
  // Free the store: user actions, physics_list and detector_description are
  // owned and deleted by the run manager, so they should not be deleted
  // in the main() program !

  delete visManager;
  delete runManager;
}

