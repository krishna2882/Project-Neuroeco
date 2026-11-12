/**
 * Project Neuroeco - creates rating Form A (anonymous, ~5 minutes). Form B has its own script.
 *
 * HOW TO USE (about 2 minutes):
 *  1. Go to https://script.google.com  ->  "New project".
 *  2. Delete the sample code, paste this whole file, click Save.
 *  3. At the top choose the function "createForm" and click Run. Approve the permission prompt
 *     (it only creates one form in your own Google Drive).
 *  4. Open "Execution log": it prints the links. Send the Form A link to ~8 people (the other form goes to ~8 different people).
 *
 * The forms do NOT collect names or emails. Nothing about the study's purpose or AI is shown to raters.
 */
var PAGES = [
 {
  "page": 1,
  "items": [
   {
    "n": 1,
    "text": "My best friend moved abroad this week, and the city seems empty. I walk past our old cafe alone every evening."
   },
   {
    "n": 2,
    "text": "This is a regular weekday for me. I am seated, the screen is on, and there is a pen and notebook beside me."
   },
   {
    "n": 3,
    "text": "Nothing in particular is happening at the moment. I am at a desk, the lights are on, and the clock shows mid afternoon."
   },
   {
    "n": 4,
    "text": "Everything is sparkling today. I am smiling at strangers, whistling down the hallway, and I could hug everyone I meet."
   },
   {
    "n": 5,
    "text": "Right now I am at my computer. I had a glass of water a few minutes ago, and the room is fairly quiet."
   },
   {
    "n": 6,
    "text": "Honestly, I am boiling inside right now. My heart is pounding, my shoulders are tight, and I want to slam a door."
   }
  ]
 },
 {
  "page": 2,
  "items": [
   {
    "n": 1,
    "text": "Today I did some laundry and answered a few emails. Later I need to buy groceries and drop off a library book."
   },
   {
    "n": 2,
    "text": "My sister had her baby this morning, a healthy little girl. I have been smiling at photos of her all day long."
   },
   {
    "n": 3,
    "text": "I am sitting at a desk near a window. I had tea earlier and will probably go to the library after this."
   },
   {
    "n": 4,
    "text": "Hi. I am filling this out between other tasks today, and the weather here is cloudy with some light wind this afternoon."
   },
   {
    "n": 5,
    "text": "I am bouncing on my toes like a child. The sky looks brighter than usual, and I cannot wipe this smile off my face."
   }
  ]
 },
 {
  "page": 3,
  "items": [
   {
    "n": 1,
    "text": "My jaw is clenched and my face is burning hot. Every little sound is grating on me right now, and my patience is gone."
   },
   {
    "n": 2,
    "text": "My grandmother passed away on Sunday. I never got to say goodbye, and I replay our last phone call in my head constantly."
   },
   {
    "n": 3,
    "text": "Right now everything is getting on my nerves. I am pacing the room, muttering under my breath, with my fists balled up."
   },
   {
    "n": 4,
    "text": "My shoulders are slumped and my voice is barely above a whisper. I am tired of everything, and the hours drag on slowly."
   },
   {
    "n": 5,
    "text": "My heart is racing in the best possible way. I have been laughing at nothing all morning, and the whole world looks wonderful."
   }
  ]
 },
 {
  "page": 4,
  "items": [
   {
    "n": 1,
    "text": "Honestly, I am sick of being messed around today. Nothing in this whole setup has gone right, and my patience is completely gone."
   },
   {
    "n": 2,
    "text": "What a wonderful day. I went for a long run by the lake, and everything about this afternoon seems so bright."
   },
   {
    "n": 3,
    "text": "I can barely get out of bed lately. The days blur together, and even small things seem far too hard to face."
   },
   {
    "n": 4,
    "text": "It is an ordinary afternoon here. I am reading the instructions on the screen and will answer once I have read them."
   },
   {
    "n": 5,
    "text": "Someone just scratched my car and drove off without a word. My jaw is clenched and I am slamming every door I pass."
   }
  ]
 },
 {
  "page": 5,
  "items": [
   {
    "n": 1,
    "text": "I am typing this with my fists clenched. My boss just yelled at me over something that was not even my fault."
   },
   {
    "n": 2,
    "text": "Everything seems empty and quiet inside me right now. I have not smiled in days, and the world looks dim and far away."
   },
   {
    "n": 3,
    "text": "Lately I move through each day like a ghost. Nothing brings any spark, and the evenings are the hardest part of all."
   },
   {
    "n": 4,
    "text": "Today everything seems to go my way. I am beaming, my steps are light, and I cannot stop laughing at little things."
   },
   {
    "n": 5,
    "text": "There is a pounding in my temples and my teeth are grinding. I have no tolerance left for anything or anyone today."
   }
  ]
 }
];

var INTRO =
  'Hi! This takes about 5 minutes. It is completely anonymous: we do not collect your name or email.\n\n' +
  'THE SITUATION\n' +
  'Imagine a simple money game between two people who never meet. For example: one person has Rs 100 and ' +
  'decides how much of it to give to the other person. Just before deciding, they receive a short message ' +
  'from the other person.\n\n' +
  'WHAT YOU DO\n' +
  'You will read short messages like that, about 5 per page. For each message, answer two quick questions:\n' +
  '  1. What feeling does the writer show?\n' +
  '  2. If you were the one deciding, would this message make you give the writer less money, about the same, or more?\n\n' +
  'There are no right or wrong answers. Go with your first feeling - most people take a few seconds per message.';

function buildForm_(name, pages) {
  var form = FormApp.create('Quick survey: how do these short messages sound? (' + name + ', about 5 minutes)');
  form.setDescription(INTRO);
  form.setCollectEmail(false);
  try { form.setRequireLogin(false); } catch (e) {}   // only matters for school/work Google accounts
  form.setAllowResponseEdits(false);
  form.setProgressBar(true);
  form.setShowLinkToRespondAgain(false);
  form.setConfirmationMessage('Thank you so much! Your answers have been saved.');

  pages.forEach(function (pg, i) {
    if (i > 0) form.addPageBreakItem().setTitle('Page ' + pg.page + ' of ' + pages.length);
    var rows = pg.items.map(function (it) { return it.n + '. "' + it.text + '"'; });
    form.addSectionHeaderItem()
      .setTitle('Page ' + pg.page + ': messages from the other person')
      .setHelpText('Imagine each message was sent to you just before you decide how much money to give the writer. ' +
                   'Each message is from a different person.');
    form.addGridItem()
      .setTitle('What feeling does the writer show? (page ' + pg.page + ')')
      .setHelpText('Pick the one that fits best. "Neutral" = no particular feeling.')
      .setRows(rows)
      .setColumns(['Neutral', 'Angry', 'Sad', 'Happy', 'Something else'])
      .setRequired(true);
    form.addGridItem()
      .setTitle('Would this message make you give the writer less money, about the same, or more? (page ' + pg.page + ')')
      .setHelpText('Compared with getting no message at all.')
      .setRows(rows)
      .setColumns(['Less', 'About the same', 'More'])
      .setRequired(true);
    var choices = pg.items.map(function (it) { return 'Message ' + it.n; });
    choices.push('None of them');
    form.addCheckboxItem()
      .setTitle('Does any message on this page sound like a threat or a promise to you? (page ' + pg.page + ')')
      .setHelpText('For example: "I will refuse anything unfair" or "If you are kind, I will pay you back". ' +
                   'Most messages are neither - if so, just tick "None of them".')
      .setChoiceValues(choices)
      .setRequired(true);
  });
  return form;
}

function createForm() {
  var form = buildForm_('Form A', PAGES);
  Logger.log('FORM A - link to send to raters: ' + form.getPublishedUrl());
  Logger.log('FORM A - edit link (keep for yourself): ' + form.getEditUrl());
}
