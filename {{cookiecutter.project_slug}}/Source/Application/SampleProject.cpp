#include "SampleProject.h"

#include <Urho3D/Engine/Engine.h>
#include <Urho3D/Input/InputEvents.h>
#include <Urho3D/Plugins/PluginApplication.h>

URHO3D_DEFINE_PLUGIN_MAIN(SampleProject);

SampleProject::SampleProject(Context* context)
    : MainPluginApplication(context)
{
}

void SampleProject::Load()
{
}

void SampleProject::Start(bool isMain)
{
    SubscribeToEvent(E_KEYDOWN, URHO3D_HANDLER(SampleProject, HandleKeyDown));
}

void SampleProject::Stop()
{
}

void SampleProject::HandleKeyDown(StringHash eventType, VariantMap& eventData)
{
    using namespace KeyDown;
    int key = eventData[P_KEY].GetInt();
    if (key == KEY_ESCAPE) {
        auto engine = GetSubsystem<Engine>();
        engine->Exit();
    }
}