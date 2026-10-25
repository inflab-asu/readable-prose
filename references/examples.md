# Before-and-after examples

Each pair shows one construction and a minimal fix. Pairs marked (systems paper) are adapted from a review of a systems paper's design section, with the system, names and details changed. Pairs marked (study) quote model output reported in the study described in paper.md. The rest are illustrative.

## Contents
1. Rare word combinations
2. Long dependencies
3. Dropped "that"
4. Stacked noun compounds
5. Nouns used as verbs
6. Inanimate subjects with animate verbs
7. Leave these alone
8. Fixes that are worse than the problem

## 1. Rare word combinations
| Before | After | Note |
|---|---|---|
| an open connection can outlive a reload that rejects new ones (systems paper) | an open connection can survive a reload that rejects new ones | "outlive" takes things with a lifetime, not events |
| A replay needs no model of the query (systems paper) | A replay needs no knowledge of what the query did | in a machine-learning paper, "model" first reads as a learned model |
| the rejected rows of Table 3 fall into two groups (systems paper) | those in Table 3 fall into two groups | rows are not rejected; requests are |
| a job that the user did not submit is also outside the quota (systems paper) | ... is also not counted against the quota | "outside the quota" reads as "over the limit" |
| This change de-risks the onboarding surface. | This change makes onboarding less risky. | |
| The cache pays rent only for hot keys. | The cache helps only for frequently read keys. | metaphor nobody in the field uses |

## 2. Long dependencies
| Before | After |
|---|---|
| The scheduler preempts within milliseconds of the deadline, not after seconds as a batch queue does, because each worker reports its progress before it takes the next task. (systems paper) | Each worker reports its progress before it takes the next task, so the scheduler preempts within milliseconds of the deadline, not after seconds as a batch queue does. |
| A request that touches nothing the cache tracks continues, such as the read with which the monitor polls its status page. (systems paper) | A request continues if it touches nothing that the cache tracks. For example, the monitor's read of its status page continues. |
| A replica that the upgrade leaves running, the other case of Section 4, stays in the old pool. (systems paper) | The other case of Section 4 is a replica that the upgrade leaves running. Such a replica stays in the old pool. |
| Users who, after the migration that we ran on the billing cluster last quarter, saw duplicate invoices should contact support. | Some users saw duplicate invoices after we migrated the billing cluster last quarter. They should contact support. |
| Before the grace period of a job that edits the load balancer's configuration, the controller reloads the balancer. (systems paper) | If a job edits the load balancer's configuration, the controller reloads the balancer before the job's grace period. |

## 3. Dropped "that"
| Before | After |
|---|---|
| the cell phone policy you are considering (study) | the cell phone policy that you are considering |
| if it touches nothing the cache tracks (systems paper) | if it touches nothing that the cache tracks |
| content an attacker wrote (systems paper) | content that an attacker wrote |
| not the memory they point to (systems paper) | not the memory that they point to |
| The results show the cache helps only for small objects. | The results show that the cache helps only for small objects. |
| We assume the network delivers messages in order. | We assume that the network delivers messages in order. |

## 4. Stacked noun compounds
| Before | After |
|---|---|
| brokerage money market funds (study) | money market funds at a brokerage |
| reader-patience budget | how much patience the reader has |
| GPU memory fragmentation mitigation strategy | a strategy to reduce fragmentation of GPU memory |
| user session timeout configuration file | the file that configures how long a user session lasts |
| model serving latency regression test suite | tests that check for regressions in serving latency |

## 5. Nouns used as verbs
| Before | After |
|---|---|
| Can you calendar it for Friday? | Can you put it on the calendar for Friday? |
| Let's footnote the caveat. | Let's mention the caveat in a footnote. |
| I'll ticket this. | I'll file a ticket for this. |
| categorize movies as speed-runnable or not (study) | sort movies by whether people can speedrun them |
| We spreadsheeted the results. | We put the results in a spreadsheet. |

## 6. Inanimate subjects with animate verbs
| Before | After |
|---|---|
| `is_file()` swallows that and returns False (study) | `is_file()` catches that exception and returns False |
| puzzle patterns where this asymmetry bites (study) | puzzles in which this asymmetry causes errors |
| At that point, the router already knows which shard the key reaches, so the planner decides on the shard itself. (systems paper) | At that point, the router has already resolved which shard the key maps to, so the planner checks the shard itself. |
| The indexer learns of an update only from a message that the broker holds. (systems paper) | The indexer receives only the messages that the broker holds. |
| The packet filter sees only a packet's header fields. (systems paper) | The packet filter receives only a packet's header fields. |
| The indexer tells an insert from an update. (systems paper) | The indexer distinguishes an insert from an update. |
| A client can ask a running daemon to make changes for it. (systems paper) | A client can request changes from a running daemon. |
| The protocol claims nothing about state derived from the cached objects. (systems paper) | The protocol guarantees nothing about state derived from the cached objects. |
| The linter hates trailing commas. | The linter rejects trailing commas. |

## 7. Leave these alone
| Text | Why it stays |
|---|---|
| the controller rolls the deploy back; the policy refuses the connection; the scheduler preempts the task | components with literal mechanical verbs are normal technical prose |
| the controller decides when to roll back | "decide" for a controller is standard systems phrasing; change it only if it reads as a metaphor in context |
| Table 2 shows that...; the reply lists each restored object | documents and messages literally show and list |
| write-ahead log; network interface card; money market fund | established multiword terms, not ad hoc stacks |
| email the authors; cache the result; log the request; host the service | established denominal verbs |
| the book I read | a very short reduced relative in informal text; "that" would sound stiff |
| pass the job to a peer (systems paper) | "hand off" would collide with the paper's defined term "handoff"; a defined term wins |

## 8. Fixes that are worse than the problem
These came from test runs of this skill. Each removed one construction and made the sentence worse in another way.

| Original | Bad fix | Better fix | What went wrong |
|---|---|---|---|
| so it decides on the replica itself | so it bases its decision on the replica itself | so it chooses the replica itself | the replacement verb phrase is stiffer than the original |
| 8% more than the quote we budgeted (email) | 8% more than the quote that we budgeted for | leave it, or "8% over budget" | restoring "that" in a short clause of a casual email sounds formal |
| a retry carries no theory of the request | a retry carries no knowledge of what the request does | a retry needs no knowledge of what the request does | the rare verb "carries" was kept when the noun was fixed |
| This trims the cognitive tax of onboarding. | (sentence deleted) | This makes onboarding easier for new operators. | deleting a sentence removes content the author chose to include |
| a README section with six fixable sentences | the section reorganized into new paragraphs with two inferred claims | each sentence fixed in place | a reorganization is a different request, and inferred claims may be wrong |
