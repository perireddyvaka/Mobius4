#!/usr/bin/env node

// Test notification functionality directly
const path = require('path');
process.chdir(path.join(__dirname));

const noti = require('./cse/noti');

async function testNotification() {
    try {
        // Create a mock request primitive for testing
        const mock_req_prim = {
            ri: '3-test-cin-' + Date.now(),
            pi: '3-20251031100851365535', // Container that has subscriptions
            ty: 4, // CIN type
            to: '/~/lmsb7lz7d1/3-20251031100851365535'
        };

        const mock_resp_prim = {
            pc: {
                'm2m:cin': {
                    rn: 'test-cin-' + Date.now(),
                    ri: mock_req_prim.ri, 
                    ty: 4,
                    con: 'test content for notification'
                }
            }
        };

        console.log('=== TESTING NOTIFICATION SYSTEM ===');
        console.log('Mock Request Primitive:');
        console.log('  RI (created resource):', mock_req_prim.ri);
        console.log('  PI (parent container):', mock_req_prim.pi);
        console.log('  TY (resource type):', mock_req_prim.ty);
        console.log();

        console.log('Testing notification with create event...');
        await noti.check_and_send_noti(mock_req_prim, mock_resp_prim, 'create');
        
        console.log('Notification test completed. Check your listener on port 8009 for notifications.');
        
    } catch (error) {
        console.error('Error testing notification:', error);
    }
}

// Run the test
testNotification();