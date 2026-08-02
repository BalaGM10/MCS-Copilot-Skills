# AXTR File Format Reference

> **Location:** `references/axtr-format-reference.md`  
> This reference explains the XML structure of Microsoft Dynamics 365 Task Recorder `.axtr` files.

---

## What is an AXTR File?

An `.axtr` file is an **XML-based output** from the **Microsoft Dynamics 365 Task Recorder**.  
It captures every user interaction (clicks, inputs, navigation) as a sequence of structured steps.

- Generated via: **Dynamics 365 → Settings → Task Recorder**
- File format: **XML** (can be opened in any text editor)
- Common use: Training documentation, process automation, RPA scripting

---

## Top-Level Structure

```xml
<?xml version="1.0" encoding="utf-8"?>
<TaskRecording>
  <TaskName>Vendor Invoice Creation</TaskName>
  <Description>Process for creating and posting a vendor invoice in Dynamics 365</Description>
  <Version>1.0</Version>
  <Steps>
    <TaskRecordingStep> ... </TaskRecordingStep>
    <TaskRecordingStep> ... </TaskRecordingStep>
    ...
  </Steps>
</TaskRecording>
```

---

## Root Element Tags

| Tag | Description | Example |
|---|---|---|
| `TaskName` | Name of the recorded process | `Vendor Invoice Creation` |
| `Description` | Summary of the process | `Creates a vendor invoice...` |
| `Version` | Recording version | `1.0` |
| `Steps` | Container for all step elements | — |

---

## Step Element Structure

Each step is wrapped in a `<TaskRecordingStep>` element:

```xml
<TaskRecordingStep>
  <StepIndex>1</StepIndex>
  <TaskStepType>UserAction</TaskStepType>
  <Caption>Navigate to Accounts Payable</Caption>
  <Comment>Click the Accounts Payable module from the main navigation menu.</Comment>
  <FormId>MainMenu</FormId>
  <ControlName>AccountsPayable</ControlName>
  <ActionType>Click</ActionType>
  <Value></Value>
  <Screenshot>base64encodedstring==</Screenshot>
</TaskRecordingStep>
```

---

## Step-Level Tags

| Tag | Description | Example |
|---|---|---|
| `StepIndex` | Sequential step number | `1`, `2`, `3` |
| `TaskStepType` | Category of step | `UserAction`, `InfoStep`, `Annotation` |
| `Caption` | Short step title | `Navigate to Accounts Payable` |
| `Comment` | Detailed instruction or help text | `Click the AP module...` |
| `FormId` | Screen or form identifier | `MainMenu`, `VendInvoiceListPage` |
| `ControlName` | Field, button, or control name | `AccountsPayable`, `NewRecord` |
| `ActionType` | Type of user interaction | `Click`, `Input`, `Select`, `Navigate` |
| `Value` | Value entered into a field (if applicable) | `INV-001`, `2026-07-10` |
| `Screenshot` | Base64-encoded screenshot image | `iVBORw0KGgoAAAA...` |

---

## Common `ActionType` Values

| ActionType | Meaning |
|---|---|
| `Click` | User clicked a button, link, or menu item |
| `Input` | User typed a value into a field |
| `Select` | User selected a dropdown or lookup value |
| `Navigate` | User navigated to a different screen or module |
| `Validate` | System or user validated a field or form |
| `Save` | User saved a record |
| `Post` | User posted or confirmed a transaction |
| `Search` | User performed a search or filter |

---

## Common `TaskStepType` Values

| TaskStepType | Meaning |
|---|---|
| `UserAction` | A direct user interaction (click, input, etc.) |
| `InfoStep` | An informational or annotation step |
| `Annotation` | A note or comment added during recording |
| `Validation` | A system validation checkpoint |

---

## Alternative Tag Names

Different versions of Dynamics 365 Task Recorder may use different tag names. The skill handles all common variants:

| Standard Tag | Known Alternatives |
|---|---|
| `TaskRecordingStep` | `Step`, `RecordingStep`, `TaskStep` |
| `TaskName` | `Name`, `Title`, `ProcessName` |
| `Caption` | `Label`, `Title`, `StepTitle` |
| `Comment` | `Description`, `Instruction`, `Note`, `Help` |
| `FormId` | `Form`, `Screen`, `Page`, `Module` |
| `ControlName` | `Control`, `Field`, `Element`, `Widget` |
| `ActionType` | `Action`, `Type`, `Interaction` |
| `Value` | `InputValue`, `FieldValue`, `Data` |
| `Screenshot` | `Image`, `ScreenCapture`, `Thumbnail` |

---

## Sample AXTR File

See `assets/sample.axtr` for a complete working example you can use to test the skill.
