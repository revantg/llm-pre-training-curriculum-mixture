{
  "addendum": "Post-yield addendum after peer exchange with AdvWishful-2. Peer withdrew their 'inherited SUPPLY_T vector' framing and returned three sharpenings; all three verified computationally. Two existing findings upgrade, one new supporting observation added. Score band unchanged.",
  "upgrades_and_additions": [
    {
      "ref": "finding 1 (STEM 250.0B) - NEW SUPPORTING TEST, closes the last charitable reading",
      "test": "Direction-and-materiality of the error on every lane left at widget 1's SUPPLY_T constant rather than re-derived from widget 9.",
      "result_table": [
        {
          "lane": "code",
          "constant": 1100,
          "inventory": 1103,
          "error_B": -3,
          "direction": "conservative",
          "ratio_at_constant": 0.435,
          "ratio_at_inventory": 0.434,
          "binding": false
        },
        {
          "lane": "stem",
          "constant": 250,
          "inventory": 146,
          "error_B": 104,
          "direction": "FLATTERS",
          "ratio_at_constant": 0.916,
          "ratio_at_inventory": 1.568,
          "binding": "YES - crosses 1.0x"
        },
        {
          "lane": "web",
          "constant": 4500,
          "inventory": 4691,
          "error_B": -191,
          "direction": "conservative",
          "ratio_at_constant": 0.15,
          "ratio_at_inventory": 0.144,
          "binding": false
        },
        {
          "lane": "longctx",
          "constant": 100,
          "inventory": 100,
          "error_B": 0,
          "direction": "none",
          "ratio_at_constant": 0.89,
          "ratio_at_inventory": 0.89,
          "binding": false
        }
      ],
      "conclusion": "STEM is not merely the only flattering error - it is the only error anywhere in the supply column that crosses the 1.0x line, i.e. the only one that changes a lane's verdict at all. The other two both UNDERSTATE supply and neither can bind (web at 0.15x, code at 0.435x). So the set of lanes the author did not re-derive contains exactly one consequential error and it points one way. Combined with the fact that he re-derived indic/reason/agentic from widget 9 at higher precision than the constant holds, and de-rated two of those three further, the 'he just trusted the course constant' defence is fully closed.",
      "severity": "FATAL (unchanged, now unanswerable)"
    },
    {
      "ref": "finding 39 - UPGRADED from WEAK to FATAL; my earlier downgrade withdrawn",
      "was": "Booking 3.0B of R1-distilled traces as Kind='real' at :173 is consistent with section 4's own existence-axis semantic (:177 defines generated rows as 'data that does not exist yet'), so poorly-chosen heading rather than false entry.",
      "peer_counter_that_defeats_it": "Sangraha synthetic (162.0B) is ALSO already-collected and also exists on disk, yet is excluded from 'real' on pure provenance grounds at :34 to produce the 113.9B figure that anchors the whole of section 2. So 'real' is a provenance word everywhere in the plan except in the one table where a distilled pool needs it to be an existence word.",
      "quantified_consequence": "Apply section 1's provenance semantic consistently and the 3.0B distilled reserve moves to generated: 'Reserve = 22.0B real/derived + 8.0B generated (27%)' becomes 19.0B + 11.0B = 36.7% generated - a 1.38x change to a number section 4 publishes in bold.",
      "verdict": "Either :173 is wrong or the 113.9B anchoring section 2 is wrong. The document cannot have both.",
      "severity": "FATAL"
    },
    {
      "ref": "finding 2 (116.0B vs 130.7B) - TIGHTENED",
      "was": "Same quantity stated twice, 12.6% apart; README labels 116.0B 'stale'.",
      "now": "Neither stated value is correct. Against 152.1B once distilled CoT is booked (18.4B served in the main run + 3.0B anneal reserve), :157's 130.7B is -14.1% and :314's 116.0B is -23.7%. Both understate, in the same direction. The sentence carrying the wrong-er of the two is the sentence certifying that every figure is 'computed rather than asserted'.",
      "severity": "FATAL"
    }
  ],
  "peer_exchange_resolution": {
    "peer": "AdvWishful-2",
    "peer_withdrew": "Their claim that all seven SOLUTION supply values match SUPPLY_T 'to the digit'. Verified false for three of seven: indic 275.9 vs 0.276T, reason 85.1 vs 0.085T, agentic 0.627 vs 0.00063T - each carries a digit the constant does not, and each is the exact itemised sum of widget 9. Only code, stem and web sit at the constant's rounding; longctx agrees with both.",
    "i_withdrew": "My WEAK downgrade of the Kind='real' finding, on the peer's provenance-vs-existence inconsistency argument, which is correct and which I verified costs a section-4 headline.",
    "net": "No open disagreements. Both reviewers converge on the same structural headline: every inflation sits in a lane the author did not audit; the four numbers on his own 'Attack first' list (:345) are all audited numbers; :345 is a map of completed work, not of weak points.",
    "band_agreement": "AdvWishful-2 355-395, mine 350-395 - the same call."
  },
  "revised_severity_counts": {
    "FATAL": 17,
    "WEAK": 19,
    "MISSING": 3
  },
  "score_band": "350-395 / 500",
  "to_move_up_one_band": "Rebuild the 'Unique supply' column of section 1 line-by-line against widget_9_dataset_inventory.html instead of widget 1's SUPPLY_T - STEM 250.0B -> 146B (0.92x -> 1.57x), code net of the 53.4B the long-context lane draws from the same pool (1.32x -> 1.47x), long-context after the same 32.9% file-level retention the code lane pays (0.89x -> ~1.49x), and agentic organic net of the three datasets widget 9 labels synthetic (73.4x -> 93.5x) - then state which lanes change verdict. STEM is the only error in that column that crosses the 1.0x line, and the three lanes already re-derived from widget 9 prove the author can do this, which is exactly why skipping it reads as directional rather than accidental."
}