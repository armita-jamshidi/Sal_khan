# Narration: How the Residency Match System Actually Works

<!--
DRAFT for review. Based on the notes brief, the fact check (sources.md) and
the outline (outline.md). Read it out loud once before recording.

Format rules (common/narration.py):
- Each `## scene_id` block belongs to one scene.
- Each paragraph is one voiceover line, so one recording take.
- HTML comments like this one are never spoken.
- TODO-VERIFY notes in square brackets are stripped from the spoken text but listed by
  todo_verify_notes(), so a final render can refuse to run while any remain.
- The `algorithm` block must keep exactly five paragraphs, in order, because
  AlgorithmScene reads its lines by position.
-->

## hook

At noon on Match Day in March, tens of thousands of medical students find out, all at the same moment, where they'll spend the next several years.

Many of them tear open an envelope. Inside is a hospital name, and a city they may have never lived in.

In 2026, more than fifty-three thousand people applied for about forty-four thousand spots.

And one computer program decided all of it. So how do you make that fair?

By the end of this video, you'll be able to run it yourself, by hand.

## problem

Let's shrink it down. Four applicants: Ana, Ben, Cy and Dee.

And three programs: City, Mercy and Lake. City is bigger, so it has two seats. Mercy and Lake have one each.

Every applicant ranks the programs. Ana loves Mercy most, then City, then Lake.

And every program ranks the applicants too. Mercy's favorite is Dee, then Ana.

Both sides have opinions, and they don't always agree.

So who should go where?

## blocking_pair

Here's the obvious idea. Give everyone their first choice, and flip a coin when two people want the same seat.

Ana and Ben both want Mercy. Ben wins the coin flip, so Ana gets her second choice, City.

Looks fine. But look at Ana and Mercy. Ana would rather be at Mercy. And Mercy would rather have Ana than Ben.

That's a blocking pair: an applicant and a program who both prefer each other over what they got. Textbooks also call it an instability.

And a blocking pair is trouble. Those two have every reason to make a side deal and ignore the system.

That actually happened. Before 1952, hospitals made offers earlier and earlier, then switched to exploding offers. By 1950, some gave students less than twelve hours to say yes.

So we want a matching with no blocking pairs at all. That's called a stable matching. How do we find one?

## algorithm

Here's the whole algorithm. Every applicant asks their favorite program. Each program says maybe to the best applicants it's seen so far, up to its number of seats, and says no to everyone else. Then anyone without a maybe asks their next choice.

Round one. Everyone asks their top choice. Ana asks Mercy, and Mercy says maybe. Ben asks Mercy too. But Mercy likes Ana more, and it only has one seat, so Ben gets a no. Cy asks City, and City says maybe. Dee asks Lake, and Lake says maybe. Notice that nobody has said yes yet. A maybe is just a placeholder.

Round two. Now watch what happens when someone better shows up. Ben moves on to his second choice and asks Lake. But Lake is already holding Dee, and it only has one seat. Lake checks its list. It likes Ben more than Dee, so it swaps. Ben gets the maybe, and Dee gets bumped back into line.

Round three. Dee asks her next choice, City. City is holding Cy, but it has two seats, so there's room. Dee gets a maybe.

And now nobody is left to ask. So every maybe becomes a yes. That's why it's called deferred acceptance: nobody says a real yes until the very end.

## stability

But wait. Could a blocking pair be hiding in this result?

Take Ben. He'd rather be at Mercy than at Lake.

But Ben asked Mercy first. Mercy said no, because it had Ana, and it liked Ana more.

And programs only ever trade up. So Mercy still has someone it likes more than Ben. No deal.

Same for Dee. She'd rather be at Lake, but Lake bumped her for Ben, and it still has Ben.

That argument works for everyone. If you'd rather be somewhere, you already asked, and they already turned you down for someone better.

So there's never a blocking pair. That's what fair means here: nobody has a reason to go around the system.

## who_proposes

Now here's the twist. What if the programs did the asking instead?

Same people, same rankings. This time City asks Ana and Ben, Mercy asks Dee, and Lake asks Ana, who turns it down. Then Lake asks Cy.

The result is stable too. But it's completely different. Every applicant ends up somewhere else, and Ben, Cy and Dee all get their last choice.

That's the rule. The side that asks gets its best possible stable outcome, and the side that waits gets its worst. [TODO-VERIFY: program-side "worst" with capacities; standard result for responsive preferences, Roth and Sotomayor 1990]

And here's the kicker. The very first Match, back in 1952, was in effect the version where hospitals ask. Ten years before Gale and Shapley even wrote this algorithm down.

So for decades, the hospitals got their best stable outcome. In 1997, the program that runs the Match voted to switch to applicants asking, starting with the 1998 Match.

## real_world

The real Match is a little fancier. It runs the Roth–Peranson algorithm, which is deferred acceptance plus extras.

The big one is couples. Two doctors can apply together, so they end up in the same city.

With couples, a perfect stable answer isn't even guaranteed to exist. But in practice, the algorithm finds one.

And in 2012, Alvin Roth and Lloyd Shapley won the Nobel Prize in Economics for this work.

## outro

So, three things. Ask your favorite. A maybe isn't a yes until the end. And whoever does the asking comes out ahead.

Next time, we'll pick another famous algorithm and run it by hand, just like this one.
