# case-02: unguarded user creation

- Behavior tested: distinguish an existing validation safeguard from a reachable invalid write.
- Source: mock application, originally recorded in this repository's fixture pair.
- Scope: complete synchronous entry-point and persistence path; no code diff.

Follow the [case template](../../../../templates/case/README.md): fill inputs,
establish expected behavior, grade, and retain each attempt.

| Part | Location |
| --- | --- |
| Reviewer task | [input/task.md](input/task.md) |
| Public requirements | [input/requirements.md](input/requirements.md) |
| Application code | [input/materials/mock-app/](input/materials/mock-app) |
| Evaluator answer | [expected.md](expected.md) |
| Grading | [grading.md](grading.md) |
| Recorded attempts | [results/](results) |

The preparation helper produces the historical flat `project/` workspace from
these inputs. Do not expose expected behavior, grading, or results to the reviewer.
