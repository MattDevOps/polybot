#!/usr/bin/env python3
"""
Polymarket Alpha Scanner Bot - FIXED VERSION
Handles actual Polymarket API response format
"""

import os
import json
import time
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

# Configuration
POLYMARKET_API = "https://gamma-api.polymarket.com"
PERPLEXITY_API = "https://api.perplexity.ai/chat/completions"
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY", "")

# Alpha scoring thresholds - LOWERED FOR BETTER RESULTS
MIN_LIQUIDITY = 5000   # Minimum $5k liquidity
MIN_VOLUME_24H = 1000  # Minimum $1k 24h volume
MAX_SPREAD = 0.10      # Maximum 10% spread
MIN_ALPHA_SCORE = 60   # Minimum alpha score (0-100)


class Verdict(Enum):
    STRONG_BUY = "STRONG_BUY"
    BUY = "BUY"
    NEUTRAL = "NEUTRAL"
    REJECT = "REJECT"


@dataclass
class Market:
    id: str
    question: str
    description: str
    end_date: str
    liquidity: float
    volume_24h: float
    yes_price: float
    no_price: float
    category: str
    url: str
    outcomes: List[str]


@dataclass
class AlphaSignal:
    market: Market
    alpha_score: float
    edge_type: str
    reasoning: str
    mispricing_estimate: float
    

@dataclass
class ResearchedPlay:
    market: Market
    alpha_signal: AlphaSignal
    research_summary: str
    key_findings: List[str]
    risk_factors: List[str]
    verdict: Verdict
    confidence: float
    recommended_position: Optional[str]
    position_size: Optional[str]
    timestamp: str


class PolymarketScanner:
    """Scans Polymarket for all active markets"""
    
    def __init__(self):
        self.base_url = POLYMARKET_API
        
    def get_active_markets(self) -> List[Market]:
        """Fetch all active markets from Polymarket"""
        try:
            # Get markets that are still open
            response = requests.get(
                f"{self.base_url}/markets",
                params={
                    "closed": "false",
                    "limit": 500,
                    "archived": "false"
                },
                timeout=30
            )
            response.raise_for_status()
            markets_data = response.json()
            
            print(f"API returned {len(markets_data)} markets")
            
            markets = []
            for m in markets_data:
                try:
                    # Handle string values that need to be converted to float
                    liquidity = float(m.get("liquidity", 0)) if m.get("liquidity") else 0
                    volume_24h = float(m.get("volume_24hr", 0)) if m.get("volume_24hr") else 0
                    
                    # Get outcome prices - handle both string and float
                    outcome_prices = m.get("outcome_prices", ["0.5", "0.5"])
                    if isinstance(outcome_prices, list) and len(outcome_prices) >= 2:
                        yes_price = float(outcome_prices[0]) if outcome_prices[0] else 0.5
                        no_price = float(outcome_prices[1]) if outcome_prices[1] else 0.5
                    else:
                        yes_price = 0.5
                        no_price = 0.5
                    
                    # Parse market data
                    market = Market(
                        id=m.get("condition_id", m.get("id", "")),
                        question=m.get("question", "Unknown"),
                        description=m.get("description", ""),
                        end_date=m.get("end_date_iso", m.get("endDate", "")),
                        liquidity=liquidity,
                        volume_24h=volume_24h,
                        yes_price=yes_price,
                        no_price=no_price,
                        category=m.get("category", m.get("groupItemTitle", "Other")),
                        url=f"https://polymarket.com/event/{m.get('slug', m.get('market_slug', ''))}",
                        outcomes=m.get("outcomes", ["Yes", "No"])
                    )
                    
                    # Filter out markets that don't meet basic criteria
                    if market.liquidity >= MIN_LIQUIDITY and market.end_date:
                        markets.append(market)
                        print(f"  ✓ {market.question[:60]}... (L:${market.liquidity:,.0f}, V:${market.volume_24h:,.0f})")
                except (KeyError, ValueError, IndexError, TypeError) as e:
                    print(f"  ✗ Error parsing market: {e}")
                    continue
                    
            print(f"\n✓ Found {len(markets)} active markets meeting criteria")
            return markets
            
        except Exception as e:
            print(f"Error fetching markets: {e}")
            import traceback
            traceback.print_exc()
            return []


class AlphaDetector:
    """Identifies markets with high alpha potential"""
    
    def calculate_alpha_score(self, market: Market) -> Optional[AlphaSignal]:
        """Calculate alpha score based on various factors"""
        
        score = 0
        reasons = []
        edge_type = "UNKNOWN"
        mispricing = 0.0
        
        # 1. Spread analysis (tighter spread = more efficient market)
        spread = abs(market.yes_price - market.no_price)
        if spread < 0.02:
            score += 15
        elif spread > MAX_SPREAD:
            score -= 20
            
        # 2. Liquidity score
        if market.liquidity > 100000:
            score += 25
            reasons.append("High liquidity ($100k+)")
        elif market.liquidity > 50000:
            score += 15
            reasons.append("Good liquidity ($50k+)")
        elif market.liquidity > 20000:
            score += 10
            reasons.append("Decent liquidity ($20k+)")
        elif market.liquidity < 10000:
            score -= 5
            
        # 3. Volume momentum
        if market.liquidity > 0:
            volume_to_liquidity = market.volume_24h / market.liquidity
            if volume_to_liquidity > 0.5:
                score += 20
                reasons.append("High volume momentum")
                edge_type = "MOMENTUM"
            elif volume_to_liquidity > 0.2:
                score += 10
                reasons.append("Good volume")
            
        # 4. Pricing inefficiency detection
        # Markets near 50/50 are often inefficient
        if 0.45 <= market.yes_price <= 0.55:
            score += 15
            reasons.append("Market uncertainty - high alpha potential")
            edge_type = "UNCERTAINTY"
            
        # Extreme pricing might indicate strong conviction or mispricing
        if market.yes_price > 0.85 or market.yes_price < 0.15:
            score += 10
            reasons.append("Extreme pricing - potential overreaction")
            edge_type = "MEAN_REVERSION"
            mispricing = abs(market.yes_price - 0.5)
            
        # 5. Time to expiry bonus (more time = more research value)
        try:
            end_date = datetime.fromisoformat(market.end_date.replace('Z', '+00:00'))
            days_remaining = (end_date - datetime.now(end_date.tzinfo)).days
            
            if 7 <= days_remaining <= 60:
                score += 15
                reasons.append(f"{days_remaining} days to expiry - optimal timeframe")
            elif days_remaining < 3:
                score -= 15
                reasons.append("Too close to expiry")
            elif days_remaining > 60:
                score += 5
                reasons.append(f"{days_remaining} days remaining")
        except:
            pass
            
        # 6. Category bonuses (some categories have more edge)
        high_edge_categories = ["Politics", "Sports", "Crypto", "Business"]
        if market.category in high_edge_categories:
            score += 10
            reasons.append(f"High-edge category: {market.category}")
            
        # Normalize score to 0-100
        alpha_score = max(0, min(100, score + 50))
        
        if alpha_score < MIN_ALPHA_SCORE:
            return None
            
        return AlphaSignal(
            market=market,
            alpha_score=alpha_score,
            edge_type=edge_type,
            reasoning=" | ".join(reasons) if reasons else "Market meets minimum criteria",
            mispricing_estimate=mispricing
        )
    
    def rank_markets(self, markets: List[Market]) -> List[AlphaSignal]:
        """Rank all markets by alpha potential"""
        signals = []
        
        for market in markets:
            signal = self.calculate_alpha_score(market)
            if signal:
                signals.append(signal)
                
        # Sort by alpha score descending
        signals.sort(key=lambda x: x.alpha_score, reverse=True)
        return signals


class PerplexityResearcher:
    """Uses Perplexity to research market theses"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = PERPLEXITY_API
        
    def research_market(self, signal: AlphaSignal) -> Dict[str, Any]:
        """Conduct deep research on a market using Perplexity"""
        
        market = signal.market
        
        # Construct research prompt
        prompt = f"""You are a prediction market analyst. Research the following market and provide a detailed analysis:

MARKET: {market.question}
DESCRIPTION: {market.description}
CURRENT PRICE: Yes={market.yes_price:.2%}, No={market.no_price:.2%}
CATEGORY: {market.category}
EXPIRES: {market.end_date}

ALPHA SIGNAL:
- Score: {signal.alpha_score}/100
- Edge Type: {signal.edge_type}
- Initial Reasoning: {signal.reasoning}

Please provide:
1. **Current State**: What's the latest information on this topic?
2. **Key Factors**: What are the main factors that will determine the outcome?
3. **Base Rate Analysis**: What do historical precedents suggest?
4. **Market Thesis**: Is the current price accurate or mispriced? Why?
5. **Risk Factors**: What could invalidate the thesis?
6. **Verdict**: STRONG_BUY, BUY, NEUTRAL, or REJECT
7. **Recommended Position**: If buying, which outcome and why?
8. **Confidence Level**: 0-100%

Be specific, cite sources, and focus on actionable insights."""

        try:
            if not self.api_key:
                # Fallback to basic analysis if no API key
                return self._fallback_analysis(signal)
                
            response = requests.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "sonar-pro",
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.2,
                    "max_tokens": 2000
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                research_text = result["choices"][0]["message"]["content"]
                return self._parse_research(research_text, signal)
            else:
                print(f"Perplexity API error: {response.status_code}")
                return self._fallback_analysis(signal)
                
        except Exception as e:
            print(f"Research error: {e}")
            return self._fallback_analysis(signal)
    
    def _parse_research(self, research_text: str, signal: AlphaSignal) -> Dict[str, Any]:
        """Parse Perplexity response into structured data"""
        
        # Extract verdict
        verdict = Verdict.NEUTRAL
        if "STRONG_BUY" in research_text or "Strong Buy" in research_text:
            verdict = Verdict.STRONG_BUY
        elif "BUY" in research_text or "Buy" in research_text:
            verdict = Verdict.BUY
        elif "REJECT" in research_text or "Reject" in research_text:
            verdict = Verdict.REJECT
            
        # Extract confidence (look for percentage)
        confidence = 50.0
        for line in research_text.split('\n'):
            if "confidence" in line.lower() or "%" in line:
                try:
                    # Find numbers followed by %
                    import re
                    match = re.search(r'(\d+)%', line)
                    if match:
                        confidence = float(match.group(1))
                        break
                except:
                    pass
        
        # Extract key findings
        key_findings = []
        risk_factors = []
        
        lines = research_text.split('\n')
        in_findings = False
        in_risks = False
        
        for line in lines:
            line = line.strip()
            if "key factor" in line.lower() or "main factor" in line.lower():
                in_findings = True
                in_risks = False
            elif "risk" in line.lower() or "could invalidate" in line.lower():
                in_findings = False
                in_risks = True
            elif line.startswith('-') or line.startswith('•') or line.startswith('*'):
                if in_findings and len(key_findings) < 5:
                    key_findings.append(line[1:].strip())
                elif in_risks and len(risk_factors) < 5:
                    risk_factors.append(line[1:].strip())
        
        # Default findings if none extracted
        if not key_findings:
            key_findings = ["See research summary for details"]
        if not risk_factors:
            risk_factors = ["Standard market risks apply"]
            
        return {
            "summary": research_text,
            "verdict": verdict,
            "confidence": confidence,
            "key_findings": key_findings,
            "risk_factors": risk_factors,
            "recommended_position": self._extract_position(research_text)
        }
    
    def _extract_position(self, text: str) -> Optional[str]:
        """Extract recommended position from research"""
        text_lower = text.lower()
        if "buy yes" in text_lower or "long yes" in text_lower:
            return "YES"
        elif "buy no" in text_lower or "long no" in text_lower:
            return "NO"
        return None
    
    def _fallback_analysis(self, signal: AlphaSignal) -> Dict[str, Any]:
        """Provide basic analysis when Perplexity is unavailable"""
        return {
            "summary": f"Market shows {signal.edge_type} edge with alpha score {signal.alpha_score}/100. "
                      f"{signal.reasoning}. Manual research recommended.",
            "verdict": Verdict.NEUTRAL,
            "confidence": 50.0,
            "key_findings": [signal.reasoning],
            "risk_factors": ["Automated analysis only - requires manual verification"],
            "recommended_position": None
        }


class AlphaBot:
    """Main orchestrator for the alpha scanning bot"""
    
    def __init__(self, perplexity_key: str, max_research: int = 10):
        self.scanner = PolymarketScanner()
        self.detector = AlphaDetector()
        self.researcher = PerplexityResearcher(perplexity_key)
        self.max_research = max_research
        
    def run_daily_scan(self) -> List[ResearchedPlay]:
        """Run complete scanning and research pipeline"""
        
        print("=" * 80)
        print("POLYMARKET ALPHA BOT - DAILY SCAN")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        # Step 1: Scan all markets
        print("\n[1/4] Scanning active markets...")
        markets = self.scanner.get_active_markets()
        print(f"✓ Found {len(markets)} active markets")
        
        # Step 2: Detect alpha opportunities
        print("\n[2/4] Detecting alpha opportunities...")
        signals = self.detector.rank_markets(markets)
        print(f"✓ Identified {len(signals)} markets with alpha potential")
        
        if not signals:
            print("\n⚠ No alpha opportunities found matching criteria")
            print("   Try lowering MIN_ALPHA_SCORE or MIN_LIQUIDITY in the code")
            return []
        
        # Step 3: Research top opportunities
        print(f"\n[3/4] Researching top {min(self.max_research, len(signals))} opportunities...")
        researched_plays = []
        
        for i, signal in enumerate(signals[:self.max_research], 1):
            print(f"\n  [{i}/{min(self.max_research, len(signals))}] Researching: {signal.market.question[:60]}...")
            
            research = self.researcher.research_market(signal)
            
            play = ResearchedPlay(
                market=signal.market,
                alpha_signal=signal,
                research_summary=research["summary"],
                key_findings=research["key_findings"],
                risk_factors=research["risk_factors"],
                verdict=research["verdict"],
                confidence=research["confidence"],
                recommended_position=research["recommended_position"],
                position_size=self._calculate_position_size(signal.alpha_score, research["confidence"]),
                timestamp=datetime.now().isoformat()
            )
            
            researched_plays.append(play)
            
            # Rate limiting
            if i < min(self.max_research, len(signals)):
                time.sleep(2)
        
        print(f"\n✓ Completed research on {len(researched_plays)} opportunities")
        
        # Step 4: Generate report
        print("\n[4/4] Generating report...")
        self._generate_report(researched_plays)
        
        return researched_plays
    
    def _calculate_position_size(self, alpha_score: float, confidence: float) -> str:
        """Calculate recommended position size based on scores"""
        combined = (alpha_score + confidence) / 2
        
        if combined >= 85:
            return "LARGE (5-10% of portfolio)"
        elif combined >= 75:
            return "MEDIUM (2-5% of portfolio)"
        elif combined >= 65:
            return "SMALL (0.5-2% of portfolio)"
        else:
            return "MICRO (<0.5% of portfolio)"
    
    def _generate_report(self, plays: List[ResearchedPlay]):
        """Generate comprehensive report"""
        
        # Create report directory
        os.makedirs("reports", exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # JSON report
        json_path = f"reports/alpha_report_{timestamp}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump([asdict(play) for play in plays], f, indent=2, default=str)
        
        # Latest report for dashboard (original bot specific)
        latest_path = "reports/original_latest.json"
        with open(latest_path, 'w', encoding='utf-8') as f:
            json.dump([asdict(play) for play in plays], f, indent=2, default=str)

        # Also write to latest_report.json for backward compatibility
        compat_path = "reports/latest_report.json"
        with open(compat_path, 'w', encoding='utf-8') as f:
            json.dump([asdict(play) for play in plays], f, indent=2, default=str)

        # Write to public/ directory for Vercel dashboard
        os.makedirs("public", exist_ok=True)
        report_data = [asdict(play) for play in plays]
        for fname in ["original_latest.json", "serious_latest.json"]:
            with open(f"public/{fname}", 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, default=str)
        
        # Human-readable report
        txt_path = f"reports/alpha_report_{timestamp}.txt"
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write("=" * 100 + "\n")
            f.write("POLYMARKET ALPHA PLAYS - DAILY REPORT\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 100 + "\n\n")
            
            # Summary
            strong_buys = [p for p in plays if p.verdict == Verdict.STRONG_BUY]
            buys = [p for p in plays if p.verdict == Verdict.BUY]
            
            f.write(f"SUMMARY:\n")
            f.write(f"  Total Opportunities Analyzed: {len(plays)}\n")
            f.write(f"  Strong Buys: {len(strong_buys)}\n")
            f.write(f"  Buys: {len(buys)}\n")
            f.write(f"  Pass/Neutral: {len(plays) - len(strong_buys) - len(buys)}\n\n")
            
            # Detailed plays
            for i, play in enumerate(plays, 1):
                f.write("\n" + "=" * 100 + "\n")
                f.write(f"PLAY #{i}\n")
                f.write("=" * 100 + "\n\n")
                
                f.write(f"MARKET: {play.market.question}\n")
                f.write(f"URL: {play.market.url}\n")
                f.write(f"Category: {play.market.category}\n")
                f.write(f"Expires: {play.market.end_date}\n\n")
                
                f.write(f"CURRENT PRICING:\n")
                f.write(f"  YES: {play.market.yes_price:.1%}\n")
                f.write(f"  NO: {play.market.no_price:.1%}\n")
                f.write(f"  Liquidity: ${play.market.liquidity:,.0f}\n")
                f.write(f"  24h Volume: ${play.market.volume_24h:,.0f}\n\n")
                
                f.write(f"ALPHA ANALYSIS:\n")
                f.write(f"  Alpha Score: {play.alpha_signal.alpha_score}/100\n")
                f.write(f"  Edge Type: {play.alpha_signal.edge_type}\n")
                f.write(f"  Reasoning: {play.alpha_signal.reasoning}\n\n")
                
                f.write(f"VERDICT: {play.verdict.value}\n")
                f.write(f"Confidence: {play.confidence:.0f}%\n")
                if play.recommended_position:
                    f.write(f"Recommended Position: {play.recommended_position}\n")
                f.write(f"Position Size: {play.position_size}\n\n")
                
                f.write(f"KEY FINDINGS:\n")
                for finding in play.key_findings:
                    f.write(f"  • {finding}\n")
                f.write(f"\n")
                
                f.write(f"RISK FACTORS:\n")
                for risk in play.risk_factors:
                    f.write(f"  • {risk}\n")
                f.write(f"\n")
                
                f.write(f"RESEARCH SUMMARY:\n")
                f.write(f"{play.research_summary}\n")
        
        print(f"\n✓ Reports generated:")
        print(f"  - {json_path}")
        print(f"  - {txt_path}")
        
        # Quick summary to console
        print("\n" + "=" * 80)
        print("QUICK SUMMARY")
        print("=" * 80)
        
        for i, play in enumerate(plays[:5], 1):  # Top 5
            verdict_emoji = {
                Verdict.STRONG_BUY: "🟢",
                Verdict.BUY: "🟡",
                Verdict.NEUTRAL: "⚪",
                Verdict.REJECT: "🔴"
            }
            
            print(f"\n{i}. {verdict_emoji[play.verdict]} {play.verdict.value} - {play.market.question[:70]}")
            print(f"   Alpha: {play.alpha_signal.alpha_score}/100 | Confidence: {play.confidence:.0f}% | {play.position_size}")
            if play.recommended_position:
                print(f"   → BUY {play.recommended_position} at {getattr(play.market, f'{play.recommended_position.lower()}_price'):.1%}")


def main():
    """Main entry point"""
    
    # Get API key from environment
    api_key = os.getenv("PERPLEXITY_API_KEY", "")
    
    if not api_key:
        print("\n⚠ WARNING: No PERPLEXITY_API_KEY found in environment")
        print("Set it with: export PERPLEXITY_API_KEY='your-key-here'  (Linux/macOS)")
        print("            setx PERPLEXITY_API_KEY 'your-key-here'    (Windows)")
        print("Bot will run with limited analysis capabilities\n")
    
    # Initialize and run bot
    bot = AlphaBot(
        perplexity_key=api_key,
        max_research=10  # Research top 10 opportunities
    )
    
    plays = bot.run_daily_scan()
    
    print("\n" + "=" * 80)
    print("✓ SCAN COMPLETE - Check reports/ directory for full analysis")
    print("=" * 80)


if __name__ == "__main__":
    main()
