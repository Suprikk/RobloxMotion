-- PoseReceiverLocal (LocalScript)
-- Taruh di: StarterPlayer > StarterPlayerScripts
-- 
-- Fungsi: Poll data dari relay server via RemoteFunction,
-- terus apply ke karakter pake IKControl
--
-- Setup:
-- 1. Aktifin HttpService di Game Settings > Security
-- 2. Jalanin relay.py di PC
-- 3. Buka controller.html di browser
-- 4. Playtest di Studio

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")

local getPoseData = ReplicatedStorage:WaitForChild("GetPoseData")
local player = Players.LocalPlayer
local character = player.Character or player.CharacterAdded:Wait()
local humanoid = character:WaitForChild("Humanoid")
local hrp = character:WaitForChild("HumanoidRootPart")

-- ================================
-- CONFIG
-- ================================
local LERP = 0.15  -- smoothing karakter (0=diam, 1=snap)
local MOVE_SPEED = 0.5  -- kecepatan gerak karakter
local JUMP_COOLDOWN = 1.0  -- detik antar lompat
-- ================================

local animate = character:FindFirstChild("Animate")
if animate then animate.Enabled = false end

task.wait(1)

-- State
local lastAction = "idle"
local lastJumpTime = 0
local latestData = { action = "idle" }
local isFetching = false

-- Poll data dari server
task.spawn(function()
	while true do
		if not isFetching then
			isFetching = true
			local ok, data = pcall(function()
				return getPoseData:InvokeServer()
			end)
			if ok and data then
				latestData = data
			end
			isFetching = false
		end
		task.wait(0.05) -- 20fps poll
	end
end)

-- Apply aksi ke karakter
RunService.Heartbeat:Connect(function(dt)
	local action = latestData.action or "idle"
	local now = tick()

	if action == "jump" then
		if now - lastJumpTime > JUMP_COOLDOWN then
			humanoid.Jump = true
			lastJumpTime = now
		end

	elseif action == "left" then
		local cf = hrp.CFrame
		hrp.CFrame = cf + cf:VectorToWorldSpace(Vector3.new(-MOVE_SPEED * dt * 60, 0, 0))

	elseif action == "right" then
		local cf = hrp.CFrame
		hrp.CFrame = cf + cf:VectorToWorldSpace(Vector3.new(MOVE_SPEED * dt * 60, 0, 0))

	elseif action == "down" then
		-- Jongkok — bisa dikustomisasi sesuai game mechanic
		humanoid.WalkSpeed = 0
	end

	-- Reset walkspeed kalau idle
	if action ~= "down" then
		humanoid.WalkSpeed = 16
	end

	lastAction = action
end)

print("Head Motion Controller aktif!")
