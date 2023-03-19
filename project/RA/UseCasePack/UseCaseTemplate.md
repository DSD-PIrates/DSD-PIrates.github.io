

## Case: Name of the Use Case

| Author   | Version | Statue    | Date       |
| -------- | ------- | --------- | ---------- |
| Somebody | 1       | Unaudited | 2023-03-19 |

### Brief Introduction

Insert a 1-2 sentence description of this use case. Be sure to include a starts when / ends when statement to clarify the beginning and ending points of the scope of this process or piece of functionality.

### Actors

List any roles or systems involved with this process or use case. A person or system fulfilling a role will be the actor in one of the steps.

- Actor 1
- Actor 2

### Pre-Conditions

List anything that must be true before this process or functionality begins. Preconditions should be states that a system can validate to be true. A common example is that a specific Actor has logged into the System.

- Cond 1
- Cond 2

### Basic Flow

The basic flow is the normal course of events, otherwise called the “happy path.” Ask yourself, what happens most of the time and you’ll discover the steps that belong here. You’ll want your basic flow to cover the full scope of activities between the starts when and ends when.

1. Step 1
2. Step 2

### Exception Flows

An alternate flow is a variation from the basic flow. Alternatives can be triggered at any step in the basic flow and often reinsert the actors back into the basic flow. 

An exception flow is an error, or a negative condition. When an exception is encountered, it prevents the process from finishing through to its conclusion until it’s addressed.

Number your alternate and exception flows to indicate the step at which the variation occurs. For example, a variation on step 3 could be listed as 3a and a second variation as 3b, and so forth.

Describe the alternate functionality and then identify at what step in the basic flow this variation picks back up. For exception flows that result in the use case ending, simply write, “Use Case Ends.”

- 1a -
- 1b -

### Post Conditions

Post-conditions indicate what must be true of the state of the system after the steps of the use case are complete. These should be true for the basic flow and all alternate flows. Exception flows may have different post-conditions or none at all.

### Supplemental Requirements

This is a special section I use to hold miscellaneous requirements related to the use case. Often you’ll find BAs including a Business Rules section or other collection of information related to the use case. These may or may not be actual requirements – you’ll want to establish a clear pattern and communicate that clearly and ensure it’s consistent with how your organization documents this type of requirement. I’ve also used this section to capture the most salient decisions and notes so they are stored right with the use case for future consideration. 

### Revision History

| Version | Date       | Author   | Description      | Status    |
| ------- | ---------- | -------- | ---------------- | --------- |
| 1       | 2023-03-19 | Somebody | Original Version | Unaudited |

