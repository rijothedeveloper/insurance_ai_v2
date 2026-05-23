def run_payout_agent(claim):
   
   deductible = 500
   
   payout = claim['estimated_damage'] - deductible
   if payout < 0:
        payout = 0
   return {
        "estimated_payout": payout,
    }