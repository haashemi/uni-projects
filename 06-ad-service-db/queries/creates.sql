-- Create Users
insert into users (name, phone, national_code, role) values
    ('Aref Nikoo'              , '9177008899', '5556667778', 'user'),
    ('Ali Hashemi'             , '9229119000', '3332221110', 'admin'),
    ('MohammadReza Benham Azad', '9367468696', '8886665551', 'admin');

-- Create Ads
insert into ads (user_id, name, audiences, image_url, target_url, since_date, until_date) values
    (
        (select (u.id) from users u where u.national_code = '5556667778'),
        'Bazitory',
        array['gaming'],
        'https://bazitory.com/banner.png',
        'https://bazitory.com',
        '2026-06-01',
        '2026-08-31'),
    (
        (select (u.id) from users u where u.national_code = '3332221110'),
        'HXLab',
        array['programming'],
        'https://hxlab.ir/banner.png',
        'https://hxlab.ir',
        '2026-06-01',
        '2026-08-31'
    );

-- Create Payments
insert into payments(ad_id, user_id, status, gateway, amount, transaction_id, gateway_data) values
    (
        (select a.id from ads a where a.name = 'Bazitory'),
        (select u.id from users u where u.national_code = '5556667778'),
        'completed',
        'zarinpal',
        120000,
        'e54cddfb-9281-4f03-be63-13297f6f63dc',
        null
    ),
    (
        (select a.id from ads a where a.name = 'HXLab'),
        (select u.id from users u where u.national_code = '3332221110'),
        'pending',
        'zarinpal',
        120000,
        '7f951904-b098-4c81-ae9f-0d0049c30328',
        null
    );

-- Create AdClicks
insert into ad_clicks (ad_id, hash, asn, asn_name, asn_country, platform, browser) values
    ((select a.id from ads a where a.name = 'Bazitory'), 'we0c2ursd9w8urvn9w8un', 'as15169', 'TCI'     , 'ir' , 'windows', 'chrome'),
    ((select a.id from ads a where a.name = 'Bazitory'), 'sdfc2ursd9w8urvn9w8un', 'as13335', 'IRANCELL', 'ir' , 'ios'    , 'safari'),
    ((select a.id from ads a where a.name = 'Bazitory'), 'wsvc2ursd9w8urvn9w8un', null     ,  null     ,  null, 'android', 'chrome mobile'),
    ((select a.id from ads a where a.name = 'Bazitory'), 'sd9hcru24nv290ujn4usn', 'as7922',  'RIGHTEL' , 'ir' , 'macos'  , 'firefox'),
    ((select a.id from ads a where a.name = 'Bazitory'), '9csunw98urv4n9bu983vd', 'as28573', 'ASIATECH', 'ir' , 'android', 'samsung browser'),
    ((select a.id from ads a where a.name = 'HXLab'   ), '09evunas09udvqdqdjkbs', 'as4134' , 'SHATEL'  , 'ir' , 'windows', 'edge');
