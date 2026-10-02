#pragma once

#include <Urho3D/Engine/Application.h>

using namespace Urho3D;

/// Main class that hosts the application.
class SampleProject : public ExecutablePlugin
{
    URHO3D_OBJECT(SampleProject, ExecutablePlugin);

public:
    explicit SampleProject(Context* context);

    /// Initialize plugin.
    void Load() override;
    /// Start game.
    void Start(bool isMain) override;
    /// Stop game.
    void Stop() override;

private:
    void HandleKeyDown(StringHash eventType, VariantMap& eventData);
};