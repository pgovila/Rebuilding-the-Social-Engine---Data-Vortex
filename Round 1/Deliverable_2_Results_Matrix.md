# DELIVERABLE 2: EXPECTED RESULTS LAYOUT MATRIX
# Data Vortex Competition — Aaruush '26, Round 1, Phase 2
# Selected: E2 (Easy) | M5 (Medium) | H5 (Hard)

---

## E2 Result Matrix: Top 10 Most Engaged Posts

**Output Structure**: 10 rows, sorted by `total_engagement DESC`. Column `engagement_rank` uses `DENSE_RANK()`.

| Rank | post_id | user_id | Platform | Text Preview | Likes | Shares | Comments | Total Engagement | Location | Followers |
|------|---------|---------|----------|-------------|-------|--------|----------|------------------|----------|-----------|
| 1 | ycjj5zzt7mvx | user_d9971ba6 | Instagram | Coca-Cola HolidaySpecial is fantastic! Can't wait to see... | 4,983 | 1,919 | 991 | **7,893** | Dubai, UAE | 13,964 |
| 2 | wo7py9aljg3t | user_o8le7hqf | Reddit | Attended the Nike LaunchWave event yesterday. Best purchas... | 4,864 | 1,981 | 948 | **7,793** | Paris, France | 13,313 |
| 3 | gmoeib832zbs | user_pe5yckyb | Facebook | Should I upgrade about Apple's iPhone 15? @TechHelp... | 4,902 | 1,880 | 982 | **7,764** | Madrid, Spain | 33,737 |
| 4 | 5kvuyvf38nqx | user_z0feut2e | YouTube | Just tried the Sprite from Coca-Cola. Worth every penny... | 4,923 | 1,971 | 861 | **7,755** | Milan, Italy | 30,461 |
| 5 | pvfl3d8hj7jd | user_csluibwk | Instagram | Just tried the Eero WiFi from Amazon. Highly recommend... | 4,989 | 1,840 | 909 | **7,738** | Tokyo, Japan | 19,091 |
| 6 | tdgjjylpua20 | user_8nvzxsuj | NaN | Comparing Adidas Samba to the competition. Had issues... | 4,979 | 1,932 | 812 | **7,723** | Vancouver, Canada | 36,383 |
| 7 | tne7s3o4l4wd | user_lr3fagdl | Instagram | Just unboxed my new Coke Zero from Coca-Cola. Had issues... | 4,931 | 1,903 | 878 | **7,712** | Paris, France | 21,509 |
| 8 | a1kiwl618kzy | user_aaiari8o | Facebook | Just tried the Zoom Pegasus from Nike. Wouldn't recommend... | 4,811 | 1,952 | 920 | **7,683** | Rome, Italy | 16,038 |
| 9 | fp89q1ickn9w | user_h4lueh1i | Twitter | NaN | 4,740 | 1,933 | 955 | **7,628** | Sydney, Australia | 17,902 |
| 10 | 5n161ir5hhhr | user_u98jwp3f | YouTube | Just unboxed my new NMD from Adidas. Not worth the money... | 4,751 | 1,981 | 878 | **7,610** | Chicago, USA | 49,936 |

### Column Definitions
| Column | Type | Description |
|--------|------|-------------|
| engagement_rank | INTEGER | DENSE_RANK by total_engagement DESC |
| post_id | TEXT | Unique post identifier |
| user_id | TEXT | Author's user ID (FK to users) |
| platform | TEXT | Social platform (nullable) |
| text_preview | TEXT | First 80 chars of post text |
| likes | INTEGER | Like count (non-null, post-filter) |
| shares | INTEGER | Share/repost count |
| comments | INTEGER | Comment count |
| total_engagement | INTEGER | likes + shares + comments |
| location | TEXT | User's registered location |
| follower_count | INTEGER | User's follower count |

---

## M5 Result Matrix: Top 20 Suspicious Engagement Posts

**Output Structure**: 20 rows, sorted by `shares DESC`. Key derived columns: `share_surplus`, `share_pct_of_total`.
**Total suspicious posts in dataset**: **1,209** (10.1% of posts with valid likes)

| Rank | post_id | user_id | Platform | Text Preview | Likes | Shares | Comments | L+C | Surplus | Share% | Location | Followers |
|------|---------|---------|----------|-------------|-------|--------|----------|-----|---------|--------|----------|-----------|
| 1 | euvr0r10wrj6 | user_irfxbf0q | Facebook | Just unboxed my new Zoom Pegasus from Nike... | 453 | 2,000 | 408 | 861 | **1,139** | 69.9% | Johannesburg, SA | 3,238 |
| 2 | 2xcg9ld7du67 | user_6w7t1ijr | Twitter | Just tried the Kindle from Amazon... | 1,425 | 1,999 | 440 | 1,865 | 134 | 51.7% | Milan, Italy | 27,442 |
| 3 | qq86lkjrfzlt | user_wouds22l | YouTube | Just unboxed my new RAV4 from Toyota... | 897 | 1,999 | 850 | 1,747 | 252 | 53.4% | Los Angeles, USA | 44,825 |
| 4 | oiszojqm6qnn | user_rscyqide | Instagram | Just unboxed my new Vision Pro from Apple... | 390 | 1,999 | 858 | 1,248 | **751** | 61.6% | Shanghai, China | 4,478 |
| 5 | sjv1fkkjr8e1 | user_evp5iscs | NaN | NaN | 1,524 | 1,998 | 129 | 1,653 | 345 | 54.7% | Shanghai, China | 20,700 |
| 6 | rryxmp0nra55 | user_nf5l9rnd | Instagram | Comparing Microsoft Xbox Series X... | 981 | 1,997 | 958 | 1,939 | 58 | 50.7% | Johannesburg, SA | 34,045 |
| 7 | zvj4ja8bp4xx | user_zmk7o7v0 | NaN | Just saw an ad for Coca-Cola Coke Zero... | 1,503 | 1,997 | 338 | 1,841 | 156 | 52.0% | Mexico City, MX | 14,414 |
| 8 | x8wq022t0pa5 | user_eatb59cy | NaN | NaN | 1,380 | 1,997 | 201 | 1,581 | 416 | 55.8% | Mexico City, MX | 39,881 |
| 9 | f2e5kdfldedz | user_kk1qdsq3 | NaN | Has anyone experienced connectivity issues... | 447 | 1,997 | 641 | 1,088 | **909** | 64.7% | New York, USA | 32,189 |
| 10 | lx50tyodyt6m | user_4ol58cyf | Instagram | Samsung ReferralBonus is decent!... | 1,545 | 1,996 | 63 | 1,608 | 388 | 55.4% | Lyon, France | 22,618 |
| 11 | 8leyamlw9c72 | user_7rdiojrn | Reddit | Comparing Amazon Halo Band... | 947 | 1,994 | 331 | 1,278 | 716 | 60.9% | Mumbai, India | 40,870 |
| 12 | mgv7p46wzpek | user_653h4bmg | Reddit | Just tried the Diet Pepsi from Pepsi... | 252 | 1,993 | 971 | 1,223 | **770** | 62.0% | Berlin, Germany | 38,484 |
| 13 | mgjoprfiflsm | user_8relh62l | Facebook | Just saw an ad for Google Pixel Watch... | 803 | 1,992 | 644 | 1,447 | 545 | 57.9% | Munich, Germany | 1,151 |
| 14 | ib1a4n09l99i | user_dcrkgrb5 | Reddit | NaN | 632 | 1,992 | 728 | 1,360 | 632 | 59.4% | Singapore | 27,599 |
| 15 | u1aa801qvxeu | user_q2stxtlj | NaN | Just saw an ad for Amazon Echo Dot... | 162 | 1,992 | 306 | 468 | **1,524** | 81.0% | Mexico City, MX | 44,195 |
| 16 | 0nsga7zrxpvt | user_c7t5ufm1 | YouTube | Attended the Samsung ValentinesDeals event... | 390 | 1,991 | 848 | 1,238 | 753 | 61.7% | Tokyo, Japan | 30,697 |
| 17 | 8d1dbq225yud | user_mpu4oig7 | Instagram | Frustrated with my new Fire TV from Amazon!... | 539 | 1,991 | 544 | 1,083 | 908 | 64.8% | Osaka, Japan | 23,515 |
| 18 | 6s9mxoemn488 | user_x87qma0e | Twitter | Attended the Microsoft DigitalTransformation... | 169 | 1,991 | 856 | 1,025 | **966** | 66.0% | Lagos, Nigeria | 39,223 |
| 19 | lit2hyqg0v0l | user_xn2a0g8z | Facebook | Nike BackToSchool is subpar!... | 14 | 1,990 | 769 | 783 | **1,207** | 71.8% | Shanghai, China | 45,029 |
| 20 | twgx52qb72eo | user_x24wilk1 | YouTube | Cannot believe with my new Air Force 1... | 462 | 1,989 | 636 | 1,098 | 891 | 64.4% | London, UK | 35,907 |

### Column Definitions
| Column | Type | Description |
|--------|------|-------------|
| suspicion_rank | INTEGER | ROW_NUMBER by shares DESC |
| likes_plus_comments (L+C) | INTEGER | likes + comments (the comparison baseline) |
| share_surplus (Surplus) | INTEGER | shares - (likes + comments): the anomaly magnitude |
| share_pct_of_total (Share%) | REAL | shares / (likes+shares+comments) * 100 |

---

## H5 Result Matrix: Data Anomaly Identification

### Anomaly Category Summary

| Anomaly Type | Record Count | Affected Users | % of Raw Data (12,360) |
|-------------|-------------|----------------|------------------------|
| MISSING_PLATFORM | 1,846 | 1,060 | 14.94% |
| MISSING_TEXT | 1,746 | 1,017 | 14.13% |
| HTML_CONTAMINATION | 1,004 | 720 | 8.12% |
| NEGATIVE_LIKES | 525 | 435 | 4.25% |
| **TOTAL ANOMALIES** | **5,121** | **--** | **41.44%** |

> Additional: 352 duplicate post_ids detected in raw data.

### Sample Records per Category (Top 5 Each)

**Output Structure**: 20 rows (5 per category), sorted by `anomaly_type ASC, row_within_category ASC`.
Window function `COUNT(*) OVER (PARTITION BY anomaly_type)` provides `category_total`.

#### NEGATIVE_LIKES (525 records)
| # | post_id | user_id | Platform | Flagged Value | Description |
|---|---------|---------|----------|---------------|-------------|
| 1 | 005g54tmt26m | user_oo2yuqwk | Facebook | -997.0 | Impossible negative engagement value |
| 2 | 01kgwhi645er | user_0xmoolhz | NaN | -3630.0 | Impossible negative engagement value |
| 3 | 07pmruq4kog9 | user_yhkk65jx | Twitter | -4126.0 | Impossible negative engagement value |
| 4 | 0c0tc7wbhqdu | user_m2ziq5ox | Instagram | -1165.0 | Impossible negative engagement value |
| 5 | 0cd8ztjdq57w | user_0ovhak73 | YouTube | -3962.0 | Impossible negative engagement value |

#### MISSING_PLATFORM (1,846 records)
| # | post_id | user_id | Platform | Flagged Value | Description |
|---|---------|---------|----------|---------------|-------------|
| 1 | 0066x8nnmouc | user_uioec9tu | NaN | NaN | Platform metadata is absent |
| 2 | 00u9otx16xfc | user_vc1szta6 | NaN | NaN | Platform metadata is absent |
| 3 | 01kgwhi645er | user_0xmoolhz | NaN | NaN | Platform metadata is absent |
| 4 | 02b0vyoya4hz | user_38xako3d | NaN | NaN | Platform metadata is absent |
| 5 | 033i6hfsrdo8 | user_1cz5m9ov | NaN | NaN | Platform metadata is absent |

#### MISSING_TEXT (1,746 records)
| # | post_id | user_id | Platform | Flagged Value | Description |
|---|---------|---------|----------|---------------|-------------|
| 1 | 00pk8aa72o8x | user_i5gyaj59 | Instagram | \<NULL\> | Post body is absent |
| 2 | 014e8jqloj6h | user_cw087eow | Facebook | \<NULL\> | Post body is absent |
| 3 | 01gbk9id4v75 | user_slqlepta | Reddit | \<NULL\> | Post body is absent |
| 4 | 033i6hfsrdo8 | user_1cz5m9ov | NaN | \<NULL\> | Post body is absent |
| 5 | 034s727kuo8m | user_vfxs1pry | YouTube | \<NULL\> | Post body is absent |

#### HTML_CONTAMINATION (1,004 records)
| # | post_id | user_id | Platform | Flagged Value | Description |
|---|---------|---------|----------|---------------|-------------|
| 1 | 003s4ulm32tk | user_nwe87ftw | Reddit | \<div\> tag found | Raw HTML tag in text |
| 2 | 0066x8nnmouc | user_uioec9tu | NaN | \<br\> tag found | Raw HTML tag in text |
| 3 | 02vdvvsovgsk | user_xnin9vng | Instagram | &amp; entity found | Unescaped HTML entity |
| 4 | 030vdql1vwxl | user_mc45jax7 | Facebook | &amp; entity found | Unescaped HTML entity |
| 5 | 033nh4sa358q | user_xiajv4r3 | Instagram | \<div\> tag found | Raw HTML tag in text |
