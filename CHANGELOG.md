# Changelog

## [Unreleased](https://github.com/aih/FlatGov/tree/HEAD)

[Full Changelog](https://github.com/aih/FlatGov/compare/2021-05-24...HEAD)

**Closed issues:**

- Overview section and Committees and Sponsors section buttons should be positioned at the bottom of the sections [\#393](https://github.com/aih/FlatGov/issues/393)

## [2021-05-24](https://github.com/aih/FlatGov/tree/2021-05-24) (2021-05-24)

[Full Changelog](https://github.com/aih/FlatGov/compare/v0.3.1...2021-05-24)

**Fixed bugs:**

- 'No data available' statements not showing  [\#353](https://github.com/aih/FlatGov/issues/353)

**Closed issues:**

- Home and Bill Page - Change background color [\#394](https://github.com/aih/FlatGov/issues/394)
- Cosponsors table 'This Congress' tab shows the full list of cosponsors [\#381](https://github.com/aih/FlatGov/issues/381)
- Normalize section total score for display [\#379](https://github.com/aih/FlatGov/issues/379)
- Metadata conversion not completed for some bills  [\#378](https://github.com/aih/FlatGov/issues/378)
- Cosponsors table shows a single sponsor of bills in both House and Senate [\#375](https://github.com/aih/FlatGov/issues/375)
- Add bill number \(e.g. 116hr200\) as a column in the CSV table for the CRS [\#364](https://github.com/aih/FlatGov/issues/364)
- Run CRS update + CSV as a nightly Celery task [\#363](https://github.com/aih/FlatGov/issues/363)
- For title matching, remove leading text of the form '117 HR 447 IH: ' [\#359](https://github.com/aih/FlatGov/issues/359)
- Add 'incorporated by' and 'incorporates' to relatedness criteria [\#355](https://github.com/aih/FlatGov/issues/355)
- Rename Context tabs [\#350](https://github.com/aih/FlatGov/issues/350)
- Develop About Us Page [\#348](https://github.com/aih/FlatGov/issues/348)
- Access to `crs/csv-report` times out \(we have ~6000 records\) [\#346](https://github.com/aih/FlatGov/issues/346)
- Review main and ensure enhancements have been added [\#344](https://github.com/aih/FlatGov/issues/344)
- Update docs and link to navigation bar [\#336](https://github.com/aih/FlatGov/issues/336)
- Issue with the logic of "Sponsors of Related Measures"  [\#326](https://github.com/aih/FlatGov/issues/326)
- Add column to indicate whether a cosponsor is no longer in Congress [\#322](https://github.com/aih/FlatGov/issues/322)
- Get cosponsors of related bills \(update\) [\#319](https://github.com/aih/FlatGov/issues/319)
- Create Celery task to update cosponsors and committees [\#298](https://github.com/aih/FlatGov/issues/298)
- Put examples of search formats below the search bar & changes to reflect wireframe [\#272](https://github.com/aih/FlatGov/issues/272)
- Scoring document similarity [\#267](https://github.com/aih/FlatGov/issues/267)
- Monthly View on Calendar should start on Monday [\#257](https://github.com/aih/FlatGov/issues/257)
- Add Text that explains that there is not a document available for Understand the Context Section [\#249](https://github.com/aih/FlatGov/issues/249)
- When the user is on a bill page, the Bill tab in the nav should be highlighted [\#245](https://github.com/aih/FlatGov/issues/245)
- Document the SAP scrapers for Trump and Biden [\#230](https://github.com/aih/FlatGov/issues/230)
- Understand the Context UI Fix [\#181](https://github.com/aih/FlatGov/issues/181)
- Future improvements for 'similar bills' [\#178](https://github.com/aih/FlatGov/issues/178)
- Add "Currently in Congress" column  to the "Sponsors of Related Measures" section [\#108](https://github.com/aih/FlatGov/issues/108)
- UI update for "Overview" section on the bill page [\#102](https://github.com/aih/FlatGov/issues/102)
- Bill title should be left aligned with all the boxes [\#100](https://github.com/aih/FlatGov/issues/100)
- Add "Compare" text button under the "Compare Bill Text" column.  [\#89](https://github.com/aih/FlatGov/issues/89)
- Change search UI on Home Page [\#83](https://github.com/aih/FlatGov/issues/83)
- The list of related bills in the top left panel does not always match the table of related bills [\#64](https://github.com/aih/FlatGov/issues/64)
- On the Bills page, change the order of tabs in the "Understand the Context" section  [\#63](https://github.com/aih/FlatGov/issues/63)
- Collect cboCostEstimates from data.json for each bill [\#53](https://github.com/aih/FlatGov/issues/53)
- Document the `bills` table and how it relates to govtrack tables [\#50](https://github.com/aih/FlatGov/issues/50)
- Sources for 'in Focus' information  [\#1](https://github.com/aih/FlatGov/issues/1)

**Merged pull requests:**

- Feature/buttons 393 [\#396](https://github.com/aih/FlatGov/pull/396) ([ayeshamk](https://github.com/ayeshamk))
- Feature/background 394 [\#395](https://github.com/aih/FlatGov/pull/395) ([ayeshamk](https://github.com/ayeshamk))
- Filter cosponsor by Congress \#381 [\#384](https://github.com/aih/FlatGov/pull/384) ([aih](https://github.com/aih))
- Fix for \#379. Normalize score [\#380](https://github.com/aih/FlatGov/pull/380) ([aih](https://github.com/aih))
- Fixes \#375 [\#376](https://github.com/aih/FlatGov/pull/376) ([aih](https://github.com/aih))
- Feature/simlar reasons update [\#374](https://github.com/aih/FlatGov/pull/374) ([aih](https://github.com/aih))
- Handle new 'reason' form [\#372](https://github.com/aih/FlatGov/pull/372) ([aih](https://github.com/aih))
- Update CSV writer for CRS [\#371](https://github.com/aih/FlatGov/pull/371) ([aih](https://github.com/aih))
- Fix 'Rank' column for cosponsors [\#370](https://github.com/aih/FlatGov/pull/370) ([aih](https://github.com/aih))
- home page UI changes [\#369](https://github.com/aih/FlatGov/pull/369) ([ayeshamk](https://github.com/ayeshamk))
- Feature/container UI changes ayesha [\#367](https://github.com/aih/FlatGov/pull/367) ([ayeshamk](https://github.com/ayeshamk))
- Feature/similarbills matrix [\#365](https://github.com/aih/FlatGov/pull/365) ([aih](https://github.com/aih))
- Weini [\#362](https://github.com/aih/FlatGov/pull/362) ([aih](https://github.com/aih))
- autocomplete and csv export updated [\#356](https://github.com/aih/FlatGov/pull/356) ([aih](https://github.com/aih))
- Feature/committees alignment fixed ayesha [\#354](https://github.com/aih/FlatGov/pull/354) ([ayeshamk](https://github.com/ayeshamk))
- Revert "Feature/no data msg2" [\#352](https://github.com/aih/FlatGov/pull/352) ([aih](https://github.com/aih))
- Feature/enhancements ayesha 2 [\#351](https://github.com/aih/FlatGov/pull/351) ([ayeshamk](https://github.com/ayeshamk))
- Fix calendar key [\#349](https://github.com/aih/FlatGov/pull/349) ([aih](https://github.com/aih))
- Feature/no data msg2 [\#347](https://github.com/aih/FlatGov/pull/347) ([aih](https://github.com/aih))
- Standardize styling when table does not have data [\#345](https://github.com/aih/FlatGov/pull/345) ([aih](https://github.com/aih))
- Fix calendar-key styling [\#343](https://github.com/aih/FlatGov/pull/343) ([aih](https://github.com/aih))
- Feature/enhancements cherrypick 2 [\#342](https://github.com/aih/FlatGov/pull/342) ([aih](https://github.com/aih))
- nav bar, home page and celery task is added [\#341](https://github.com/aih/FlatGov/pull/341) ([aih](https://github.com/aih))
- calendar UI changes [\#339](https://github.com/aih/FlatGov/pull/339) ([ayeshamk](https://github.com/ayeshamk))

## [v0.3.1](https://github.com/aih/FlatGov/tree/v0.3.1) (2021-05-01)

[Full Changelog](https://github.com/aih/FlatGov/compare/v0.3.0...v0.3.1)

**Implemented enhancements:**

- Create Celery task to update CBO data [\#213](https://github.com/aih/FlatGov/issues/213)

**Closed issues:**

- Daniel's Home Page Feedback [\#207](https://github.com/aih/FlatGov/issues/207)
- CRS reports: add a Celery task [\#173](https://github.com/aih/FlatGov/issues/173)
- UI Updates for Sponsors of Related Measures [\#147](https://github.com/aih/FlatGov/issues/147)

**Merged pull requests:**

- Docs/update and link [\#338](https://github.com/aih/FlatGov/pull/338) ([aih](https://github.com/aih))
- Docs/update and link [\#337](https://github.com/aih/FlatGov/pull/337) ([aih](https://github.com/aih))
- home UI updated [\#335](https://github.com/aih/FlatGov/pull/335) ([aih](https://github.com/aih))

## [v0.3.0](https://github.com/aih/FlatGov/tree/v0.3.0) (2021-04-27)

[Full Changelog](https://github.com/aih/FlatGov/compare/2021-03-30...v0.3.0)

**Implemented enhancements:**

- Move all scrapy scripts out of the top level of the `scrapers` directory [\#210](https://github.com/aih/FlatGov/issues/210)

**Fixed bugs:**

- Problem getting number for congress with some bills [\#329](https://github.com/aih/FlatGov/issues/329)
- CBO report: handle error with 'pubDate' [\#184](https://github.com/aih/FlatGov/issues/184)
- Skip adding text when there is no summary \(adding cosponsors\) [\#55](https://github.com/aih/FlatGov/issues/55)
- Apparent problem indexing 116hr5150 [\#43](https://github.com/aih/FlatGov/issues/43)
- Handle cosponsor names like 'Sanford D. Bishop, Jr.' which currently becomes 'Jr. Sanford D. Bishop' [\#24](https://github.com/aih/FlatGov/issues/24)

**Closed issues:**

- Search using just the bill number will populate results but the links route the user to a "page not found" page [\#327](https://github.com/aih/FlatGov/issues/327)
- Develop a download csv/xls file feature for the "Sponsors of related measures" table data [\#324](https://github.com/aih/FlatGov/issues/324)
- Remove Committee Id from both Co-Sponsors tables [\#323](https://github.com/aih/FlatGov/issues/323)
- Change 'On Assigned Committee' to 'Current Assigned Committee' [\#321](https://github.com/aih/FlatGov/issues/321)
- Add 'leadership' information to Cosponsor download [\#316](https://github.com/aih/FlatGov/issues/316)
- Remove 'Read Bill:' text [\#313](https://github.com/aih/FlatGov/issues/313)
- Short title missing in bill data [\#309](https://github.com/aih/FlatGov/issues/309)
- Set the order of cosponsors for the Committees and Cosponsors box [\#306](https://github.com/aih/FlatGov/issues/306)
- Propagate Cosponsor table to the `cosponsor_dict` in the detail.html view [\#305](https://github.com/aih/FlatGov/issues/305)
- Handle 'H.Con.Res.' in title correctly [\#304](https://github.com/aih/FlatGov/issues/304)
- Capture committee information when processing data.json for bills [\#300](https://github.com/aih/FlatGov/issues/300)
- Related Bills in Overview section - include only related bills from the current congress and change display [\#290](https://github.com/aih/FlatGov/issues/290)
- Apply ordinal in bill display filter  [\#289](https://github.com/aih/FlatGov/issues/289)
- Press statement Put Pagination in a fixed position [\#283](https://github.com/aih/FlatGov/issues/283)
- Press statements: Add Pagination navigation menu [\#281](https://github.com/aih/FlatGov/issues/281)
- Press Statements: Change architecture and show results instantly using direct API calls [\#280](https://github.com/aih/FlatGov/issues/280)
- Press Statements  [\#275](https://github.com/aih/FlatGov/issues/275)
- Read Bill button  [\#274](https://github.com/aih/FlatGov/issues/274)
- Include short title \(or truncated short title\) in typeahead search list [\#273](https://github.com/aih/FlatGov/issues/273)
- Search bar input format [\#271](https://github.com/aih/FlatGov/issues/271)
- The congress filter should be on the same line as the search bar and include arrow [\#270](https://github.com/aih/FlatGov/issues/270)
- Create scraper to update legislator information [\#268](https://github.com/aih/FlatGov/issues/268)
- Create a Celery task to update the \(Biden\) SAP scraper daily  [\#264](https://github.com/aih/FlatGov/issues/264)
- Committee and member information available from Propublica API [\#263](https://github.com/aih/FlatGov/issues/263)
- Add Committee and Party information to Sponsors [\#259](https://github.com/aih/FlatGov/issues/259)
- Provide consistent bill number display, e.g. H. R. 1500 \(116\) [\#254](https://github.com/aih/FlatGov/issues/254)
- Organize Celery tasks [\#248](https://github.com/aih/FlatGov/issues/248)
- Make Sponsor table more compatible with Govtrack [\#228](https://github.com/aih/FlatGov/issues/228)
- Remove the 'Sponsor' model from bill.models [\#227](https://github.com/aih/FlatGov/issues/227)
- Refactor CBO scraper to allow dynamic updates [\#212](https://github.com/aih/FlatGov/issues/212)
- Create Celery task for Committee Documents [\#205](https://github.com/aih/FlatGov/issues/205)
- Scrape the current Biden Statements of administration policy [\#203](https://github.com/aih/FlatGov/issues/203)
- Statements and CBO: Consider using many-to-many relation to bills [\#185](https://github.com/aih/FlatGov/issues/185)
- UI Sprint 1 \_ Bill Page "Folder" Containers [\#166](https://github.com/aih/FlatGov/issues/166)
- UI Sprint 1 \_ Bills Related to  [\#164](https://github.com/aih/FlatGov/issues/164)
- UI Sprint 1 \_ Committees and Sponsors Section [\#163](https://github.com/aih/FlatGov/issues/163)
- UI Sprint 1 \_ Overview Section  [\#161](https://github.com/aih/FlatGov/issues/161)
- Change Overview Section UI [\#155](https://github.com/aih/FlatGov/issues/155)
- Bill selection: Allow user to hit return to select the currently typed value [\#123](https://github.com/aih/FlatGov/issues/123)
- Bill summary should be a small description instead of a "read bill" button [\#101](https://github.com/aih/FlatGov/issues/101)
- Add "Export" button on right side for "Sponsors of Related Measures" and " Bills Related to" sections to download a .csv file [\#90](https://github.com/aih/FlatGov/issues/90)
- Link to Committee transcript data for bill \(no need to scrape\) [\#54](https://github.com/aih/FlatGov/issues/54)
- Develop API calls for Press statements [\#35](https://github.com/aih/FlatGov/issues/35)

**Merged pull requests:**

- Remove 'amdt' bills from search. Fixes \#327 [\#332](https://github.com/aih/FlatGov/pull/332) ([aih](https://github.com/aih))
- Feature/related cosponsors [\#331](https://github.com/aih/FlatGov/pull/331) ([aih](https://github.com/aih))
- Fix for 'None' in bill number or congress [\#330](https://github.com/aih/FlatGov/pull/330) ([aih](https://github.com/aih))
- Feature/committees cosponsors ayesha [\#328](https://github.com/aih/FlatGov/pull/328) ([ayeshamk](https://github.com/ayeshamk))
- Docs/celery update [\#325](https://github.com/aih/FlatGov/pull/325) ([aih](https://github.com/aih))
- Add Cosponsor relations to Bill model [\#320](https://github.com/aih/FlatGov/pull/320) ([aih](https://github.com/aih))
- Add committee leadership positions [\#317](https://github.com/aih/FlatGov/pull/317) ([aih](https://github.com/aih))
- Clean up fields in detail view [\#312](https://github.com/aih/FlatGov/pull/312) ([aih](https://github.com/aih))
- Update billdata [\#311](https://github.com/aih/FlatGov/pull/311) ([aih](https://github.com/aih))
- Update billdata [\#310](https://github.com/aih/FlatGov/pull/310) ([aih](https://github.com/aih))
- Bug/type abbrev [\#308](https://github.com/aih/FlatGov/pull/308) ([aih](https://github.com/aih))
- Fix for type abbrev. Closes \#304 [\#307](https://github.com/aih/FlatGov/pull/307) ([aih](https://github.com/aih))
- Feature/related bills ayesha [\#302](https://github.com/aih/FlatGov/pull/302) ([ayeshamk](https://github.com/ayeshamk))
- Feature/bill committee [\#301](https://github.com/aih/FlatGov/pull/301) ([aih](https://github.com/aih))
- Fix for \#272 [\#299](https://github.com/aih/FlatGov/pull/299) ([aih](https://github.com/aih))
- Feature/cosponsor UI [\#297](https://github.com/aih/FlatGov/pull/297) ([aih](https://github.com/aih))
- Feature/cosponsor info [\#296](https://github.com/aih/FlatGov/pull/296) ([aih](https://github.com/aih))
- Feature/crec celery [\#295](https://github.com/aih/FlatGov/pull/295) ([aih](https://github.com/aih))
- Bump django from 3.1.6 to 3.1.8 [\#294](https://github.com/aih/FlatGov/pull/294) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump django from 3.1.6 to 3.1.8 in /server\_py [\#293](https://github.com/aih/FlatGov/pull/293) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bill short titles [\#292](https://github.com/aih/FlatGov/pull/292) ([aih](https://github.com/aih))
- Convert congress to ordinals [\#291](https://github.com/aih/FlatGov/pull/291) ([aih](https://github.com/aih))
- Bump urllib3 from 1.26.3 to 1.26.4 in /server\_py [\#288](https://github.com/aih/FlatGov/pull/288) ([dependabot[bot]](https://github.com/apps/dependabot))
- search bar UI updated [\#287](https://github.com/aih/FlatGov/pull/287) ([aih](https://github.com/aih))
- Feature/read bill ayesha [\#286](https://github.com/aih/FlatGov/pull/286) ([aih](https://github.com/aih))
- Add date templates [\#284](https://github.com/aih/FlatGov/pull/284) ([aih](https://github.com/aih))
- Press statements ayesha [\#282](https://github.com/aih/FlatGov/pull/282) ([ayeshamk](https://github.com/ayeshamk))
- Feature/crec celery [\#279](https://github.com/aih/FlatGov/pull/279) ([kapphire](https://github.com/kapphire))
- Feature/readme celery [\#278](https://github.com/aih/FlatGov/pull/278) ([aih](https://github.com/aih))
- Feature/readme celery [\#277](https://github.com/aih/FlatGov/pull/277) ([aih](https://github.com/aih))
- Feature/django scrapy [\#276](https://github.com/aih/FlatGov/pull/276) ([kapphire](https://github.com/kapphire))



\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*
